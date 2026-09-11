% Reading notes: classicthesis layout, shared environments, explicit subject packages.
% See README.md and docs/MIGRATION.md for the v2 authoring interface.

\NeedsTeXFormat{LaTeX2e}[2026-06-01]
\ProvidesClass{coursenotes}[2026/09/11 v2.0.0 Reading notes]

\RequirePackage{coursecommon}
\courseworksetup{font-profile=euler}
\DeclareOption*{\expandafter\courseworkclassoption\expandafter{\CurrentOption}{report}}
\ProcessOptions\relax

\LoadClass[12pt,letterpaper]{report}

\PassOptionsToPackage{
	drafting=true,
	tocaligned=true,
	dottedtoc=true,
	manychapters=true,
	eulerchapternumbers=false,
	linedheaders=false,
	floatperchapter=true,
	eulermath=false,
	beramono=true,
	palatino=false,
	style=classicthesis
}{classicthesis}
% Load mathematics and the shared font configuration before classicthesis.
\PassOptionsToPackage{unicode}{coursemath}
\RequirePackage{coursemath}
\RequirePackage{courseenvironments}
\RequirePackage{coursefonts}
\RequirePackage{classicthesis}

\RequirePackage{etoc}                               % For \localtableofcontents
\RequirePackage{fontspec}
\RequirePackage{graphicx}                           % Used for inserting images.
\RequirePackage{hyperref}                           % Reference by name
\RequirePackage{lastpage}                           % For page count in header/footer.
\RequirePackage{nameref}
\RequirePackage{subfiles}                           % Per-chapter standalone builds
\RequirePackage{tabularx}                           % For pset heading
\RequirePackage{titlesec}                           % Section label customization
\RequirePackage{titling}                            % Title page customization
\RequirePackage{tkz-euclide}                        % For geometric figures
\RequirePackage{url}                                % Enables urls with the \url tag
\RequirePackage{xcolor}                             % Required. For setting the color of hyperlinks

%----------------------------
% Font selection is owned by coursefonts.
\RequirePackage{cleveref}
\RequirePackage[all]{hypcap}  % hypcap: Links go to object instead of caption. [Keep as last package]
% report restarts page numbering after its title page. Give page 1 only
% to the contents/body page, avoiding a duplicate title-page destination.
\AddToHook{env/titlepage/before}{\hypersetup{pageanchor=false}}
\AddToHook{env/titlepage/after}{\hypersetup{pageanchor=true}}
%----------------------------

% SI Units handling
\AddToHook{package/siunitx/after}{\sisetup{group-separator={,}}}

% Native section labels already include their chapter.

% ============= Shared macro packages =============
% The notes layout wants math tables pinned in place and pulled a little
% tighter than the problem-set layout does.



\courseenvironmentsetup{table-placement=H,table-top-skip=-2ex}

\endinput
% chktex 17
