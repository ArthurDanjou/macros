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
\addauthor{ad}{blue}
\input{macros/macros.tex}
```

The macros define mathematical notation and algorithm names. Configure editing
authors in the document preamble with `\addauthor`, as in the example above.
The shared file does not register authors or override their colors. With `article` or `report`, theorem environments use `amsthm`, share a
counter numbered by section, and default to French. With LLNCS, load only
`amsmath,amssymb` before the macros. The class's native environments, numbering,
and English default are preserved.

## French and English environments

The base names are `theorem`, `lemma`, `proposition`, `corollary`, `property`,
`definition`, `assumption`, `remark`, `example`, and `proof`. Use `\macrosenglish`
or `\macrosfrench` to select their heading language, or append `en` or `fr` to
an environment name for a local choice. The explicit variants share the base
counters and accept the same optional titles. Their language choice does not
change subsequent environments. Only headings are translated. Authors supply
the statement and any optional title in the desired language.

```tex
\begin{theoremen}[Robustness coefficient]
  Your English statement.
\end{theoremen}

\begin{theoremfr}[Coefficient de robustesse]
  Votre énoncé français.
\end{theoremfr}
```

## Subset robustness notation

All notation commands are used in math mode. A reference subset is arbitrary
and is not identified with `\honest` or `\byzset`.

| Command | Meaning |
| --- | --- |
| `\nworkers`, `\nbyz`, `\dimension` | Parameters $n$, $f$, $d$. |
| `\workerindices`, `\nreference` | $[n]$ and $n-f$. |
| `\refset`, `\refcomplement` | $\mathcal S$ and its complement $\mathcal A$. |
| `\subsets{N}{m}` | The family $\mathcal P^N_m$ of subsets of size $m$. |
| `\refsubsets`, `\refsubsetsdef` | $\mathcal P^n_{n-f}$ and its defining equality. |
| `\refmean`, `\refcoordmean{j}`, `\refvariance` | Subset mean, coordinate mean, and variance. |
| `\refmeandef`, `\refvariancedef` | Their defining equalities. |
| `\vectorspace`, `\signspace` | $\mathbb R^d$ and $\{-1,+1\}^d$. |
| `\inputvectors`, `\aggregator` | $\mathcal X$ and $F$. |
| `\kappastar{F}`, `\robustnessratio{F}` | Coefficient notation and squared error divided by subset variance. |
| `\kappastardef{F}` | Full supremum definition over real inputs and reference subsets with positive variance. |
| `\kappastardef[\signspace]{F}` | The same definition restricted to sign messages. |

The definitions reuse `\nworkers` and `\nbyz`. Changing these two commands also
updates the subset family and the supremum limits. The choice of input domain
is mathematical: a bound established on sign messages does not automatically
hold on all real inputs.

## Overleaf projects

If an Overleaf sync exchanges a subtree through Git, keep a regular copy of
`macros.tex` inside that subtree. Git does not include submodule contents in
such an exchange. Update the copy from this repository when needed.

To use a newer revision, update the submodule and commit its pointer in the
project:

```sh
git submodule update --remote macros
git add macros
git commit -m "Update shared LaTeX macros."
```


## Verification

With `pdflatex`, `pdftotext`, and `llncs.cls` available, run:

```sh
python3 tests/check.py
```

The check compiles both classes, verifies bilingual headings and optional titles,
checks that language switches are local and theorem variants share numbering,
and exercises the subset definitions with renamed parameters. Generated files
are kept in a temporary directory.
