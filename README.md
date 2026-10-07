# Shared LaTeX macros

Personal LaTeX macros shared across papers, reports, and presentations.
The initial definitions come from the M2 internship report.

## Usage

Add this repository as a submodule in a LaTeX project:

```sh
git submodule add https://github.com/ArthurDanjou/macros.git macros
git submodule update --init --recursive
```

Load the required packages before the macros in your preamble:

```tex
\usepackage{amsmath,amssymb,amsthm}
\usepackage{xcolor,hyperref,color-edits}
\input{macros/macros.tex}
```

The macros define French theorem environments numbered by section, mathematical
notation, algorithm names, and Arthur's editing commands.

To use a newer revision, update the submodule and commit its pointer in the
project:

```sh
git submodule update --remote macros
git add macros
git commit -m "Update shared LaTeX macros."
```
