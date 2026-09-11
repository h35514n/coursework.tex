% Assignments and exams: declarations, semantic references, and output profiles.
% See README.md and docs/MIGRATION.md for the v2 authoring interface.

\NeedsTeXFormat{LaTeX2e}[2026-06-01]
\ProvidesClass{coursepsets}[2026/09/11 v2.0.0 Problem sets and exams]

\RequirePackage{coursecommon}
\DeclareOption*{\expandafter\courseworkclassoption\expandafter{\CurrentOption}{article}}
\ProcessOptions\relax

% ================== Packages and Document Options ==================
\LoadClass[11pt,letterpaper]{article}
\PassOptionsToPackage{unicode}{coursemath}
\RequirePackage{coursemath}
\RequirePackage{courseenvironments}
\RequirePackage{coursefonts}


\RequirePackage[small]{caption}
\RequirePackage{fancyhdr}                           % For customizing headers/footers.
\RequirePackage{fontspec}
\RequirePackage[top=0.85in, bottom=1in, left=1in, right=1in]{geometry}
\RequirePackage{graphicx}                           % Used for inserting images.
\RequirePackage[colorlinks=true, linkcolor=navy, urlcolor=black]{hyperref}
\RequirePackage{lastpage}                           % For page count in header/footer.

\RequirePackage{nameref}
\RequirePackage[font={footnotesize}]{subcaption}
\RequirePackage{subfiles}                           % Per-pset standalone builds
\RequirePackage{tabularx}                           % For pset heading
\RequirePackage{titlesec}                           % Section label customization
\RequirePackage{titling}                            % Title page customization
\RequirePackage[titles]{tocloft}
\RequirePackage[obeyFinal, color=@todoclr, linecolor=red]{todonotes}
\RequirePackage{tkz-euclide}                        % Required for geometric figures
\RequirePackage{url}                                % Enables urls with the \url tag
\RequirePackage{xcolor}                             % Set hyperlink color
% -------------------- Late loaders -----------------------------------------
% Font selection is owned by coursefonts; no mathspec
\RequirePackage{courseassignments}
\RequirePackage{cleveref}
\RequirePackage[all]{hypcap}    % Links go to object instead of caption [keep as last]

% Fonts are selected by coursefonts.

% ==================   Appearance Settings   ==================
\definecolor{@todoclr}{gray}{0.80}   % For To-Dos. 50% brightness
\definecolor{navy}{RGB}{0,0,150}     % For coloring hyperlinks
\setlength{\parskip}{1.5ex}          % Sets space between paragraphs.
\setlength{\parindent}{0pt}          % Indent for first line of new paragraphs.

% Smaller verbatim type size
\let\VERBATIM\verbatim%
\def\verbatim{%
	\def\verbatim@font{\small\ttfamily}%
\VERBATIM}

% =============   Caption Modifications   =============
% For no visible number, use: \caption*{Unnumbered figure caption.}
\captionsetup[table]{labelformat=simple, labelsep=period, labelfont=bf}
\captionsetup[figure]{labelformat=simple, labelsep=period, labelfont=bf}
\captionsetup[subtable]{labelformat=parens, labelsep=space, labelfont=bf}
\captionsetup[subfigure]{labelformat=simple, labelsep=period, labelfont=bf}

% ================== TOC and Bookmarks setup ==================
\setcounter{tocdepth}{2}      % Set the depth of ToC to 2 (includes up to \subsections)
\hypersetup{bookmarksdepth=3} % Set the depth of PDF bookmarks to 3 (includes \subsubsections)

% ================== SI Units setup ==================
\AddToHook{package/siunitx/after}{\sisetup{group-separator={,}}}

% ============= Headers and Footers =============
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0.5pt}
\pagestyle{fancyplain}
\fancyhf{}
\lfoot{%
	\fancyplain{}{%
		\small{%
			\color{black}{%
				\courseworkvalue{course-code}%
			}
		}
	}
}
\cfoot{%
	\fancyplain{}{%
		\small{%
			% \coursename%
			\courseassignmentfooter%
		}
	}
}
\rfoot{%
	\fancyplain{}{%
		\courseproblemfooter%
	}
}

% ============= Section label customizations =============
\titleformat{\section}
[block]                      % The shape of the title (e.g., runin, left, right, etc.)
{\normalfont\Large\bfseries} % (no change)
{\thesection.}               % (no change)
{0.5em}                      % Tighten spacing
{}                           % Before-code (no change)

\titleformat{\subsection}
[block]                      % The shape of the title (e.g., runin, left, right, etc.)
{\normalfont\large\bfseries}
{}
{0em}                        % horizontal separation between label and title body
{}                           % Before-code (no change)
% Consecutive role/problem headings must reserve real vertical space.
% Negative title after-code overlaps the first problem's text.
\titlespacing*{\subsection}{0pt}{3.25ex plus 1ex minus .2ex}{1ex plus .2ex}

\titleformat{\subsubsection}
[block]                      % The shape of the title (e.g., runin, left, right, etc.)
{\normalfont}                % Format for the title
{}                           % No label (empty braces to omit numbering)
{0em}                        % Horizontal separation between label and title body
{}                           % Before-code
[\vspace{-1.5ex}]            % After-code (add vertical space after the title)


% Shared interfaces are independent of this class's heading styles.
\endinput
