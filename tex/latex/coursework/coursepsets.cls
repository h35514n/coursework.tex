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
\ProvidesClass{coursepsets}[2026/09/05 v1.0 Problem sets and exams]

\DeclareOption{summary}{\providecommand{\@solutionvis}{0}\providecommand{\@summary}{1}}
\DeclareOption{worksheet}{\providecommand{\@solutionvis}{0}}
\DeclareOption{expand}{\providecommand{\@expand}{1}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
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

% ==================     Booleans     ==================
\def\TRUE{1}
\def\FALSE{0}
\def\SHOW{1}
\def\HIDE{0}

% ================== TOC and Bookmarks setup ==================
\setcounter{tocdepth}{2}      % Set the depth of ToC to 2 (includes up to \subsections)
\hypersetup{bookmarksdepth=3} % Set the depth of PDF bookmarks to 3 (includes \subsubsections)

% ================== SI Units setup ==================
\sisetup{group-separator = {,}}

% ============= Gets Document Info, Generates Heading =============
\providecommand{\heading}[5][]{
	\thispagestyle{empty}
	\listoftodos%
	\clearpage
	\pagenumbering{arabic}
	%
	\providecommand{\assignmentname}{#1}
	\providecommand{\authorname}{#2}
	\providecommand{\coursenumber}{#3}
	\providecommand{\coursename}{#4}
	\providecommand{\duedate}{#5}
	\title{\large\coursename\\\coursenumber}
	\date{\duedate}
	\author{\authorname}
	\maketitle
	\tableofcontents
	\newpage

	\begin{minipage}{0.5\textwidth}
		\begin{flushleft}
			\authorname\\%
			\assignmentname%
		\end{flushleft}
	\end{minipage}
	\begin{minipage}{0.5\textwidth}
		\begin{flushright}
			\coursename\\
			\duedate\\
		\end{flushright}
	\end{minipage}
	\thispagestyle{empty}
}

% ============= Headers and Footers =============
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0.5pt}
\pagestyle{fancyplain}
\fancyhf{}
\lfoot{%
	\fancyplain{}{%
		\small{%
			\color{black}{%
				\coursenumber%
			}
		}
	}
}
\cfoot{%
	\fancyplain{}{%
		\small{%
			% \coursename%
			\currentchapter.~\currentchaptername%
		}
	}
}
\rfoot{%
	\fancyplain{}{%
		\currentsectionname~\thesection.\thetheproblem%
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


% ============= Problem Command =============
\newcounter{theproblem} % Problem counter for environment

\providecommand{\problem}[1][]{%
	\addtocounter{theproblem}{1}%
	\setcounter{table}{0}%
	\setcounter{figure}{0}%
	\setcounter{equation}{0}%
	\noindent%
	\ifthenelse{\isempty{#1}}%
	{\subsubsection{\textbf{Problem~\arabic{theproblem}}}}%
	{\subsubsection{\textbf{Problem~\arabic{theproblem}}.~\textit{\small{#1}}}}%
}

% ============= QED, Page Breaks After QED? =============
\providecommand{\@expand}{\HIDE}  % Default is to omit pagebreaks after the solution
\providecommand{\qqed}{\ifnum\@expand=\SHOW\\\pagebreak\else\hfill\rule{2mm}{2mm}\fi}


% ============= Solution Command =============
\providecommand{\@solutionvis}{1} % Default setting is to show solutions.
\providecommand{\@summary}{0}     % Default setting is to not format as problem summary
\providecommand{\solution}[2][\@solutionvis]{
	\ifnum#1=\SHOW%
		\vspace{0.5em}\noindent\textbf{Solution}

		#2

		\hfill\qqed\vspace{0.1em}
	\else%
		\ifnum\@summary=0
			\pagebreak%
		\else
			\vspace{4ex}
		\fi
	\fi%

}

% ============= Chapter, Section, Item Commands =============
\newcommand*{\currentchapter}{0}
\newcommand*{\currentchaptername}{}
\providecommand{\chap}[2][0]{
	\renewcommand*{\currentchapter}{#1}
	\renewcommand*{\currentchaptername}{#2}
	\setcounter{theproblem}{0}%
	\ifnum#1=0%
	\else%
		\setcounter{section}{\currentchapter}%
		\addtocounter{section}{-1}%
	\fi%
	\vspace{-1.75em}%
	\section{\currentchaptername}
}

\newcommand*{\currentsection}{0}
\newcommand*{\currentsectionname}{}
\providecommand{\sect}[2][0]{
	\renewcommand*{\currentsection}{#1}
	\renewcommand*{\currentsectionname}{#2}
	\setcounter{theproblem}{0}%
	\ifnum#1=0%
	\else%
		\setcounter{subsection}{\currentsection}%
		\addtocounter{subsection}{-1}%
	\fi%
	\vspace{-0.5em}%
	\subsection{\currentsectionname}
}

\providecommand{\subsect}[1]{\noindent\textbf{#1.}}

% ============= Insert Non-Float Image =============
\providecommand{\insertgraphic}[2][0.5\textwidth]{
	\vspace{-1em}
	\begin{center}
		\includegraphics[width=#1]{#2}
	\end{center}
	\vspace{-1em}
}



% ============= Object Numbering by Problem =============
\renewcommand{\thetable}{\thesection.\arabic{theproblem}.\arabic{table}}
\renewcommand{\thefigure}{\thesection.\arabic{theproblem}.\arabic{figure}}
\renewcommand{\theequation}{\thesection.\arabic{theproblem}.\arabic{equation}}

% ============= Shared macro packages =============
% Loaded last: everything they \RequirePackage is already loaded above,
% so the deliberate ordering (amsmath before mathspec, hypcap last
% among the layout packages) is preserved.
\RequirePackage{coursemath}
\RequirePackage{coursephys}

\endinput
% chktex 17
