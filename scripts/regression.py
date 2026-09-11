#!/usr/bin/env python3
"""Build and compare coursework fixtures without changing the installed classes."""

import argparse
from collections import Counter
import difflib
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import time

ROOT = Path(os.environ.get("COURSEWORK_TEST_ROOT", Path(__file__).resolve().parents[1])).resolve()
BASELINE = ROOT / "baseline"
CANDIDATE = ROOT / "build/candidate"
COMPARISON = ROOT / "build/comparison"
SHARED = {"coursepsets.cls", "coursenotes.cls", "coursemath.sty", "coursephys.sty"}
GLYPHS = {"coursework-scriptr.pdf", "coursework-boldr.pdf"}


def run(args, *, cwd=ROOT, env=None):
    proc = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(f"Command failed: {' '.join(map(str, args))}\n{proc.stdout}{proc.stderr}")
    return proc.stdout.strip()


def git(repo, *args):
    return run(["git", "-C", str(repo), *args])


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    temp.replace(path)


def tracked_files(repo):
    names = git(repo, "ls-files", "--cached", "--others", "--exclude-standard", "-z").split("\0")
    return {name: sha(repo / name) if (repo / name).is_file() else None
            for name in names if name}


def class_files(directory):
    return {str(p.relative_to(directory)): sha(p) for p in sorted(directory.rglob("*"))
            if p.is_file()}


def source_info(repo):
    return {"revision": git(repo, "rev-parse", "HEAD"),
            "status": git(repo, "status", "--short"), "files": tracked_files(repo)}


def build_environment(directory, epoch):
    env = os.environ.copy()
    # Trailing empty element preserves kpathsea's standard search path.
    env["TEXINPUTS"] = str(directory) + "//:" + env.get("TEXINPUTS", "") + ":"
    env["SOURCE_DATE_EPOCH"] = epoch
    env["FORCE_SOURCE_DATE"] = "1"
    return env


def resolve_classes(directory, env, *, legacy=False, source_root=ROOT):
    resolved = {}
    for name in sorted({"problemsets.cls", "notes.cls"} if legacy else SHARED | GLYPHS | {p.name for p in directory.glob("*.sty")}):
        args = ["kpsewhich", "-progname=xelatex"]
        if name in GLYPHS:
            args += ["-format=graphic/figure"]
        value = run(args + [name], env=env, cwd=source_root)
        actual = (source_root / value).resolve()
        expected = (directory / name).resolve()
        if not value or actual != expected:
            raise RuntimeError(f"Wrong class/asset resolution for {name}: {value!r}; expected {expected}")
        resolved[name] = str(actual)
    return resolved


def verify_recorder(recorder, directory, source_root=ROOT, *, legacy=False):
    """Reject an installed-class fallback, including files loaded indirectly."""
    used = set()
    names = ({"problemsets.cls", "notes.cls"} if legacy else SHARED | GLYPHS | {p.name for p in directory.rglob("*.sty")})
    for line in recorder.read_text().splitlines():
        if not line.startswith("INPUT "):
            continue
        actual = (source_root / line[6:]).resolve()
        if actual.name in names or (actual.name.startswith("course") and actual.suffix in {".sty", ".cls"}):
            expected = (directory / actual.name).resolve()
            if actual != expected:
                raise RuntimeError(f"{recorder}: loaded {actual}, expected {expected}")
            used.add(actual.name)
    required = set() if legacy else {"coursemath.sty", "coursephys.sty"}
    classes = {"problemsets.cls", "notes.cls"} if legacy else {"coursenotes.cls", "coursepsets.cls"}
    if not required <= used or not used & classes:
        raise RuntimeError(f"{recorder}: incomplete coursework inputs: {sorted(used)}")
    return sorted(used)


def expected_pdfs(source_root=ROOT):
    names = {"homework.pdf", "notes.pdf", "problems.pdf"}
    for path in (source_root / "homework").glob("*.tex"):
        names.update({f"homework/{path.stem}.pdf", f"problems/{path.stem}-problems.pdf",
                      f"worksheets/{path.stem}-worksheet.pdf"})
    names.update(f"notes/{p.stem}.pdf" for p in (source_root / "notes").glob("*.tex"))
    return sorted(names)


def warnings_in(text, directory):
    result = Counter()
    for line in text.splitlines():
        if re.search(r"Warning:|(?:Over|Under)full \\[hv]box|Missing character:|xdvipdfmx:warning:", line):
            line = line.strip().replace(str(directory), "<classes>").replace(str(ROOT), "<testbed>")
            result[line] += 1
    return result


def comparable_warnings(warnings):
    result = Counter()
    for message, count in warnings.items():
        # Parallel make jobs share stdout: TeX's progress text can precede a
        # backend warning on the same line. Preserve the actual diagnostic,
        # not the unrelated prefix. Normalize at comparison time so existing
        # frozen manifests remain intact.
        if message.startswith("PDF backend: ") and "xdvipdfmx:warning:" in message:
            message = "PDF backend: " + message[message.index("xdvipdfmx:warning:"):]
        result[message] += count
    return result


def inspect_pdf(pdf, artifact_root, dpi):
    relative = pdf.relative_to(artifact_root / "pdf")
    folder = artifact_root / "inspection" / relative.with_suffix("")
    folder.mkdir(parents=True, exist_ok=True)
    info = run(["pdfinfo", str(pdf)])
    (folder / "pdfinfo.txt").write_text(info + "\n")
    (folder / "fonts.txt").write_text(run(["pdffonts", str(pdf)]) + "\n")
    match = re.search(r"^Pages:\s+(\d+)", info, re.M)
    if not match:
        raise RuntimeError(f"Cannot read page count: {pdf}")
    pages = int(match[1])
    text_path = folder / "text.txt"
    run(["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), str(text_path)])
    run(["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(folder / "page")])
    images = sorted(folder.glob("page-*.png"), key=lambda p: int(p.stem.rsplit("-", 1)[1]))
    if len(images) != pages:
        raise RuntimeError(f"Incomplete rendering: {pdf}")
    return {"pages": pages, "pdf_sha256": sha(pdf),
            "text": str(text_path.relative_to(artifact_root)), "text_sha256": sha(text_path),
            "renders": {str(p.relative_to(artifact_root)): sha(p) for p in images}}


def snapshot_classes(artifact_root, manifest):
    """Resolve frozen bundles locally; historical absolute paths are provenance."""
    if manifest.get("frozen_fixtures"):
        directory = artifact_root / "classes"
        if manifest.get("mode") == "baseline" and not manifest.get("legacy_classes"):
            directory /= "tex/latex/coursework"
    else:
        directory = Path(manifest["class_directory"])
    if not directory.is_dir():
        raise RuntimeError(f"Class snapshot missing: {directory}")
    return directory


def check_integrity(artifact_root, manifest):
    directory = snapshot_classes(artifact_root, manifest)
    if class_files(directory) != manifest["class_files"]:
        raise RuntimeError(f"Class snapshot changed since build: {directory}")
    if manifest.get("frozen_fixtures"):
        for relative, expected in manifest["testbed"]["files"].items():
            path = artifact_root / "fixtures" / relative
            if expected is not None and (not path.is_file() or sha(path) != expected):
                raise RuntimeError(f"Fixture snapshot changed: {path}")
    for name, info in manifest["pdfs"].items():
        paths = {"pdf/" + name: info["pdf_sha256"], info["text"]: info["text_sha256"],
                 **info["renders"]}
        for relative, expected in paths.items():
            path = artifact_root / relative
            if not path.is_file() or sha(path) != expected:
                raise RuntimeError(f"Build artifact modified or missing: {path}")


def tool_versions():
    result = {}
    for tool, flag in [("xelatex", "--version"), ("latexmk", "-v"),
                       ("pdftoppm", "-v"), ("pdftotext", "-v"), ("magick", "-version")]:
        executable = shutil.which(tool)
        if executable is None:
            raise RuntimeError(f"Required tool not installed: {tool}")
        proc = subprocess.run([executable, flag], capture_output=True, text=True, check=True)
        result[tool] = {"executable": executable, "version": (proc.stdout + proc.stderr).strip()}
    return result


def build(mode, config):
    artifact_root = BASELINE if mode == "baseline" else CANDIDATE
    manifest_path = artifact_root / "manifest.json"
    if mode == "baseline" and manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        if manifest["class_revision"] != config["baseline_revision"]:
            raise RuntimeError("Existing baseline is for another revision; archive it before creating a new baseline.")
        check_integrity(artifact_root, manifest)
        print(f"Preserving baseline: {manifest_path}", flush=True)
        return
    tools = tool_versions()
    if artifact_root.exists():
        # A completed baseline is handled above and is never replaced.
        shutil.rmtree(artifact_root)
    artifact_root.mkdir(parents=True)
    legacy = mode == "baseline" and config.get("baseline_layout") == "local-classes"
    origin = ROOT if legacy else (ROOT / config["class_repository"]).resolve()
    epoch_origin = ROOT if config.get("baseline_layout") == "local-classes" else origin
    epoch = git(epoch_origin, "show", "-s", "--format=%ct", config["baseline_revision"])
    source_root = ROOT
    if mode == "baseline":
        archive = subprocess.check_output(["git", "-C", str(origin), "archive",
                                           config["baseline_revision"], *(["problemsets.cls", "notes.cls"] if legacy else ["tex/latex/coursework"])])
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            tar.extractall(artifact_root / "classes", filter="data")
        directory = artifact_root / ("classes" if legacy else "classes/tex/latex/coursework")
        for path in directory.iterdir():
            if path.is_file():
                path.chmod(0o444)
        revision = config["baseline_revision"]
        class_status = ""
        fixture_revision = config["baseline_fixture_revision"]
        archive = subprocess.check_output(["git", "-C", str(ROOT), "archive", fixture_revision])
        source_root = artifact_root / "fixtures"
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            tar.extractall(source_root, filter="data")
        # The frozen class bundle is authoritative; do not let fixture-root copies
        # shadow it through TeX's current-directory search. Original bytes also
        # remain in the revision archive and are hashed in class_files.
        if legacy:
            for name in ("problemsets.cls", "notes.cls"):
                (source_root / name).unlink()
        fixture = {"revision": fixture_revision, "status": "", "files": class_files(source_root)}
    else:
        repo = (ROOT / config["candidate_repository"]).resolve()
        directory = repo / "tex/latex/coursework"
        revision = git(repo, "rev-parse", "HEAD")
        class_status = git(repo, "status", "--short")
        fixture = source_info(ROOT)
    before = class_files(directory)
    env = build_environment(directory, epoch)
    resolved = resolve_classes(directory, env, legacy=legacy, source_root=source_root)
    command = ["make", "-k", f"-j{config['jobs']}", f"BUILD={artifact_root / 'pdf'}",
               "LATEXMKOPT=-halt-on-error", "all", "problems", "worksheets"]
    started = time.time()
    print(f"Building {mode}: {len(expected_pdfs(source_root))} PDFs; console: {artifact_root / 'build.log'}", flush=True)
    with (artifact_root / "build.log").open("w") as console:
        proc = subprocess.run(command, cwd=source_root, env=env, stdout=console, stderr=subprocess.STDOUT)
    metadata = {"mode": mode, "class_revision": revision, "class_status": class_status,
                "class_directory": str(directory), "class_files": before, "testbed": fixture,
                "resolved": resolved, "tools": tools, "source_date_epoch": epoch,
                "render_dpi": config["render_dpi"], "command": command, "frozen_fixtures": mode == "baseline",
                "legacy_classes": legacy}
    if proc.returncode:
        write_json(artifact_root / "failure.json", {**metadata, "exit_code": proc.returncode})
        raise RuntimeError(f"{mode} build failed; see {artifact_root / 'build.log'}")
    if before != class_files(directory) or (mode != "baseline" and fixture != source_info(ROOT)):
        raise RuntimeError("Sources changed during the build; rerun against stable sources.")
    expected = expected_pdfs(source_root)
    actual = sorted(str(p.relative_to(artifact_root / "pdf")) for p in (artifact_root / "pdf").rglob("*.pdf"))
    if actual != expected:
        raise RuntimeError(f"Incomplete PDF set: expected {expected}, got {actual}")
    pdfs, inputs, warnings = {}, {}, Counter()
    for index, name in enumerate(expected, 1):
        pdf = artifact_root / "pdf" / name
        inputs[name] = verify_recorder(pdf.with_suffix(".fls"), directory, source_root, legacy=legacy)
        warnings.update({f"{name}: {message}": count for message, count in
                         warnings_in(pdf.with_suffix(".log").read_text(errors="replace"), directory).items()})
        print(f"Inspecting {mode} {index}/{len(expected)}: {name}", flush=True)
        pdfs[name] = inspect_pdf(pdf, artifact_root, config["render_dpi"])
    backend = "\n".join(line for line in (artifact_root / "build.log").read_text().splitlines()
                        if "xdvipdfmx:warning:" in line)
    warnings.update({f"PDF backend: {message}": count for message, count in warnings_in(backend, directory).items()})
    write_json(artifact_root / "warnings.json", dict(warnings))
    write_json(manifest_path, {**metadata, "pdfs": pdfs, "recorder_inputs": inputs,
                               "warnings": dict(warnings), "elapsed_seconds": round(time.time() - started, 2)})
    print(f"Completed {mode}: {len(pdfs)} PDFs, {sum(p['pages'] for p in pdfs.values())} pages", flush=True)


def compare_images(left, right, diff):
    if sha(left) == sha(right):
        return 0
    diff.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(["magick", "compare", "-metric", "AE", str(left), str(right), str(diff)],
                          capture_output=True, text=True, env={**os.environ, "MAGICK_THREAD_LIMIT": "1"})
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"Image comparison failed: {proc.stderr}")
    pixels = float(proc.stderr.strip().split()[0])
    if not pixels:
        diff.unlink(missing_ok=True)
    return pixels


def compare(reference=None):
    reference = reference or BASELINE
    comparison = ROOT / "build" / ("comparison" if reference == BASELINE else "comparison-" + reference.name)
    baseline = json.loads((reference / "manifest.json").read_text())
    candidate = json.loads((CANDIDATE / "manifest.json").read_text())
    check_integrity(reference, baseline)
    check_integrity(CANDIDATE, candidate)
    if candidate["testbed"] != source_info(ROOT):
        raise RuntimeError("Candidate fixtures changed since build; run make candidate first.")
    if baseline["render_dpi"] != candidate["render_dpi"] or baseline["tools"] != candidate["tools"]:
        raise RuntimeError("Tool versions or render resolution differ; use the baseline toolchain.")
    if comparison.exists():
        shutil.rmtree(comparison)
    comparison.mkdir(parents=True)
    results = []
    for name in sorted(baseline["pdfs"].keys() | candidate["pdfs"].keys()):
        left, right = baseline["pdfs"].get(name), candidate["pdfs"].get(name)
        if left is None or right is None:
            results.append({"pdf": name, "missing": "baseline" if left is None else "candidate"})
            continue
        text_equal = left["text_sha256"] == right["text_sha256"]
        diffs = comparison / "diffs" / Path(name).with_suffix("")
        if not text_equal:
            diffs.mkdir(parents=True, exist_ok=True)
            delta = difflib.unified_diff((reference / left["text"]).read_text().splitlines(True),
                                        (CANDIDATE / right["text"]).read_text().splitlines(True),
                                        fromfile="baseline", tofile="candidate")
            (diffs / "text.diff").write_text("".join(delta))
        changed = []
        # JSON keys are sorted lexically, so page order must be restored numerically.
        order = lambda path: int(Path(path).stem.rsplit("-", 1)[1])
        lhs, rhs = sorted(left["renders"], key=order), sorted(right["renders"], key=order)
        for number, (a, b) in enumerate(zip(lhs, rhs), 1):
            pixels = compare_images(reference / a, CANDIDATE / b, diffs / f"page-{number}.png")
            if pixels:
                changed.append({"page": number, "pixels": pixels})
        results.append({"pdf": name, "baseline_pages": left["pages"], "candidate_pages": right["pages"],
                        "text_equal": text_equal, "changed_pages": changed})
    old, new = comparable_warnings(baseline["warnings"]), comparable_warnings(candidate["warnings"])
    added, removed = dict(new - old), dict(old - new)
    passed = not added and all("missing" not in row and row["text_equal"]
                              and row["baseline_pages"] == row["candidate_pages"]
                              and not row["changed_pages"] for row in results)
    report = {"passed": passed, "reference": str(reference), "baseline_revision": baseline["class_revision"],
              "candidate_revision": candidate["class_revision"],
              "baseline_testbed_revision": baseline["testbed"]["revision"],
              "candidate_testbed_revision": candidate["testbed"]["revision"],
              "existing_warnings": baseline["warnings"], "new_warnings": added,
              "resolved_warnings": removed, "pdfs": results}
    write_json(comparison / "report.json", report)
    lines = ["# Coursework comparison", "", f"Result: **{'PASS' if passed else 'DIFFERENCES'}**", "",
             f"Compared {len(results)} PDFs at {baseline['render_dpi']} dpi.", "",
             f"Baseline classes: `{baseline['class_revision']}`.",
             f"Candidate classes: `{candidate['class_revision']}`.", "",
             f"Existing warning occurrences: {sum(old.values())}; new: {sum(added.values())}; resolved: {sum(removed.values())}.", "",
             "| PDF | Pages (baseline / candidate) | Text | Changed page renders |",
             "| --- | --- | --- | --- |"]
    for row in results:
        if "missing" in row:
            lines.append(f"| {row['pdf']} | Missing from {row['missing']} | - | - |")
        else:
            lines.append(f"| {row['pdf']} | {row['baseline_pages']} / {row['candidate_pages']} | "
                         f"{'same' if row['text_equal'] else 'DIFF'} | {len(row['changed_pages'])} |")
    lines += ["", "See `report.json` for warning details and `diffs/` for text and image differences.",
              "Matching output establishes regression equivalence, not the absence of inherited layout or content issues."]
    (comparison / "report.md").write_text("\n".join(lines) + "\n")
    print(f"{'PASS' if passed else 'DIFFERENCES'}: {comparison / 'report.md'}", flush=True)
    return 0 if passed else 1


def checkpoint(name, reason):
    """Freeze a reviewed candidate, including classes and exact build inputs."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name) or not reason.strip():
        raise RuntimeError("A checkpoint needs a safe name and a review reason.")
    target = ROOT / "checkpoints" / name
    if target.exists():
        raise RuntimeError(f"Checkpoint already exists: {target}")
    manifest = json.loads((CANDIDATE / "manifest.json").read_text())
    check_integrity(CANDIDATE, manifest)
    if manifest["testbed"] != source_info(ROOT):
        raise RuntimeError("Candidate sources changed; rebuild before checkpointing.")
    shutil.copytree(CANDIDATE, target)
    classes = target / "classes"
    shutil.copytree(manifest["class_directory"], classes)
    manifest["class_directory"] = str(classes)
    manifest["review_reason"] = reason
    manifest["checkpoint"] = name
    manifest["frozen_fixtures"] = True
    for rel in manifest["testbed"]["files"]:
        source = ROOT / rel
        if source.is_file():
            destination = target / "fixtures" / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    write_json(target / "manifest.json", manifest)
    print(f"Saved immutable reference: {target}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["baseline", "candidate", "compare", "checkpoint"])
    parser.add_argument("--reference", default="baseline")
    parser.add_argument("--name")
    parser.add_argument("--reason", default="")
    args = parser.parse_args()
    config = json.loads((ROOT / "regression.json").read_text())
    (ROOT / "build").mkdir(exist_ok=True)
    with (ROOT / "build/regression.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            if args.operation == "compare":
                reference = BASELINE if args.reference == "baseline" else ROOT / "checkpoints" / args.reference
                return compare(reference)
            if args.operation == "checkpoint":
                checkpoint(args.name or "", args.reason)
                return 0
            build(args.operation, config)
            return 0
        except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
            print(f"ERROR: {error}", flush=True)
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
