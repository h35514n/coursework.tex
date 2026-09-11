"""Check rendered role-to-problem heading gaps, in PDF points."""
import subprocess
import xml.etree.ElementTree as ET


def check_heading_spacing(pdf, minimum=4.0):
    xml = subprocess.check_output(['pdftotext', '-bbox-layout', str(pdf), '-'], text=True)
    root = ET.fromstring(xml)
    ns = {'x': 'http://www.w3.org/1999/xhtml'}
    roles = {'Guide', 'Problem Set', 'Discussion'}
    found = set()
    gaps = []
    for page in root.findall('.//x:page', ns):
        lines = page.findall('.//x:line', ns)
        for index, line in enumerate(lines):
            title = ' '.join(word.text or '' for word in line.findall('x:word', ns))
            if title not in roles:
                continue
            found.add(title)
            assert index + 1 < len(lines), f'{title}: problem heading stranded on next page'
            following = lines[index + 1]
            text = ' '.join(word.text or '' for word in following.findall('x:word', ns))
            assert text.startswith('Problem '), f'{title}: expected following problem heading, got {text!r}'
            gap = float(following.attrib['yMin']) - float(line.attrib['yMax'])
            assert gap >= minimum, f'{title}: heading gap {gap:.2f}pt is below {minimum}pt'
            gaps.append((title, round(gap, 2)))
    assert found == roles, f'Missing role headings: {roles - found}'
    return gaps


if __name__ == '__main__':
    import sys
    print(check_heading_spacing(sys.argv[1]))
