% =====================================================================
% coursenotes.cls -- Reading-notes document class for coursework.
%   (Formerly notes.cls.)
%
% Layout only: classicthesis over report, plus per-chapter local TOCs.
% Math macros and physics notation come from coursemath.sty and
% coursephys.sty, loaded at the foot of this file. The old notes.cls
% was truncated mid-file and shipped no physics notation at all --
% \rcurs, \grad, \vhat and friends are now available here too.
% =====================================================================

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{coursenotes}[2026/09/05 v1.0 Reading notes]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax

\LoadClass[12pt,letterpaper]{report}

\PassOptionsToPackage{
	drafting=true,
	tocaligned=true,
	dottedtoc=true,
	manychapters=true,
	eulerchapternumbers=true,
	linedheaders=false,
	floatperchapter=true,
	eulermath=true,
	beramono=true,
	palatino=true,
	style=classicthesis
}{classicthesis}
% amssymb before classicthesis: classicthesis's eulermath option pulls in
% eulervm, and whichever of the two loads second fails on \eth.
\RequirePackage{amssymb}
\RequirePackage{classicthesis}

\RequirePackage{amsmath}
\RequirePackage{amsthm}                             % Used for theorem environments.
\RequirePackage{bigints}                            % Larger integral signs
\RequirePackage{bm}                                 % For bold math symbols
\RequirePackage{booktabs}                           % Required. Used for mathtable environment.
\RequirePackage{cleveref}                           % Reference by chapter and section
\RequirePackage[spaced, mleftright]{diffcoeff}		% For \diff and \diffp commands
\RequirePackage{enumitem}                           % Used for the enumerate environment.
\RequirePackage{etoc}                               % For \localtableofcontents
\RequirePackage{float}                              % Use H to suppress table float
\RequirePackage{fontspec}
\RequirePackage{graphicx}                           % Used for inserting images.
\RequirePackage{hyperref}                           % Reference by name
\RequirePackage{lastpage}                           % For page count in header/footer.
\RequirePackage{mathtools}                          % Loads amsmath.
\RequirePackage{nameref}
\RequirePackage{pgfkeys}                            % For mathtable environment.
\RequirePackage{siunitx}                            % For SI units.
\RequirePackage{subfiles}                           % Per-chapter standalone builds
\RequirePackage{tabularx}                           % For pset heading
\RequirePackage{titlesec}                           % Section label customization
\RequirePackage{titling}                            % Title page customization
\RequirePackage{tkz-euclide}                        % For geometric figures
\RequirePackage{url}                                % Enables urls with the \url tag
\RequirePackage{xcolor}                             % Required. For setting the color of hyperlinks
\RequirePackage{xifthen}                            % Conditional constructs

%----------------------------
\RequirePackage{mathspec}     % keep after amsmath
\RequirePackage[all]{hypcap}  % hypcap: Links go to object instead of caption. [Keep as last package]
%----------------------------

% SI Units handling
\sisetup{group-separator = {,}}

% cleveref: use prefix "\thechapter." for references to sections
\labelformat{section}{\thechapter.#1}

% ============= Shared macro packages =============
% The notes layout wants math tables pinned in place and pulled a little
% tighter than the problem-set layout does.
\providecommand{\coursemathtablestart}{\begin{table}[H]}
\providecommand{\coursemathtabletopskip}{-2ex}

\RequirePackage{coursemath}
\RequirePackage{coursephys}

\endinput
% chktex 17
