% =====================================================================
% coursepsets.cls -- Problem set / exam document class for coursework.
%   (Formerly problemsets.cls.)
%
% Layout, the \problem/\solution machinery, and headers live here.
% Math macros and physics notation come from coursemath.sty and
% coursephys.sty, loaded at the foot of this file.
%
% Options:
% final      hides to-dos
% worksheet  hides solutions and places each problem on separate page
% expand     places each problem on a separate page
% summary    hides solutions without placing problems on separate pages
% =====================================================================

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{coursepsets}[2026/09/11 v2.0.0 Problem sets and exams]

\RequirePackage{coursecommon}
\DeclareOption*{\expandafter\courseworkclassoption\expandafter{\CurrentOption}{article}}
\ProcessOptions\relax

% ================== Packages and Document Options ==================
\LoadClass[11pt,letterpaper]{article}

\RequirePackage{amssymb}
\RequirePackage{amsthm}                             % Used for theorem environments.
\RequirePackage[scaled=0.85]{beramono}
\RequirePackage{bigints}                            % Larger integral signs
\RequirePackage{bm}                                 % For boldface in math mode
\RequirePackage{booktabs}                           % Used for mathtable environment.
\RequirePackage[small]{caption}
\RequirePackage[spaced, mleftright]{diffcoeff}      % For \diff, \diffp, etc commands
\RequirePackage{enumitem}                           % Used for the enumerate environment.
\RequirePackage{fancyhdr}                           % For customizing headers/footers.
\RequirePackage{float}                              % Used for floats (tables, figures, etc.)
\RequirePackage{fontspec}
\RequirePackage[top=0.85in, bottom=1in, left=1in, right=1in]{geometry}
\RequirePackage{graphicx}                           % Used for inserting images.
\RequirePackage[colorlinks=true, linkcolor=navy, urlcolor=black]{hyperref}
\RequirePackage{lastpage}                           % For page count in header/footer.
\RequirePackage[osf,sc]{mathpazo}
\RequirePackage{mathtools}                          % Loads amsmath.
\RequirePackage{nameref}
\RequirePackage{pgfkeys}                            % For mathtable environment.
\RequirePackage{siunitx}                            % For SI units.
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
\RequirePackage{xifthen}                            % Conditional constructs
% -------------------- Late loaders -----------------------------------------
\RequirePackage{cleveref}                           % Reference by chapter and section
\RequirePackage{mathspec}
\RequirePackage[all]{hypcap}    % Links go to object instead of caption [keep as last]

% ==================   Font Settings   ==================
% \PassOptionsToPackage{osf,sc}{mathpazo}
% \PassOptionsToPackage{scaled=0.85}{beramono}
\setmainfont[Ligatures=TeX,Numbers=OldStyle]{TeX Gyre Pagella} % Palatino clone
\linespread{1.05} % a bit more for Palatino
\setmathfont{TeX Gyre Pagella Math}
\setmonofont[Scale=0.85]{DejaVu Sans Mono}
\DeclareFixedFont{\chapterNumber}{U}{eur}{b}{n}{70}

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
\sisetup{group-separator = {,}}

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
[\vspace{-4ex}]

\titleformat{\subsubsection}
[block]                      % The shape of the title (e.g., runin, left, right, etc.)
{\normalfont}                % Format for the title
{}                           % No label (empty braces to omit numbering)
{0em}                        % Horizontal separation between label and title body
{}                           % Before-code
[\vspace{-1.5ex}]            % After-code (add vertical space after the title)


% Shared interfaces are independent of this class's heading styles.
\RequirePackage{coursemath}
\RequirePackage{courseenvironments}
\RequirePackage{courseassignments}
\endinput
