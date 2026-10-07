"""Compile bilingual environments and subset notation with article and LLNCS."""
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HEADINGS = {
    "theorem": ("Théorème", "Theorem"),
    "lemma": ("Lemme", "Lemma"),
    "proposition": ("Proposition", "Proposition"),
    "corollary": ("Corollaire", "Corollary"),
    "property": ("Propriété", "Property"),
    "definition": ("Définition", "Definition"),
    "assumption": ("Hypothèse", "Assumption"),
    "remark": ("Remarque", "Remark"),
    "example": ("Exemple", "Example"),
    "proof": ("Preuve", "Proof"),
}


def check(document_class, directory):
    packages = "amsmath,amssymb" + (",amsthm" if document_class == "article" else "")
    source = (
        rf"\documentclass{{{document_class}}}" + "\n"
        r"\usepackage[T1]{fontenc}" + "\n"
        rf"\usepackage{{{packages}}}" + "\n"
        r"\usepackage{xcolor,hyperref,color-edits}" + "\n"
        rf"\input{{{ROOT / 'macros.tex'}}}" + "\n"
        r"\begin{document}\section{Checks}" + "\n"
    )
    for environment in HEADINGS:
        for language in ("fr", "en", ""):
            name = environment + language
            title = "[Optional title]" if environment != "proof" else ""
            source += (
                rf"\begin{{{name}}}{title}Statement.\label{{{name}}}\end{{{name}}}"
                + "\n"
            )
    source += r"""
\[\refsubsetsdef\]
\[\refmeandef,\qquad\refvariancedef\]
\[\kappastardef{\aggregator}\]
\[\kappastardef[\signspace]{G}\]
\renewcommand{\nworkers}{N}
\renewcommand{\nbyz}{b}
\[\refsubsetsdef,\qquad\sumn x_i\]
\typeout{PARAMETERS: \nworkers,\nbyz,\nreference}
\end{document}
"""
    path = directory / (document_class + ".tex")
    path.write_text(source)
    for _ in range(2):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", path.name],
            cwd=directory, capture_output=True, text=True,
        )
        if result.returncode:
            raise RuntimeError(result.stdout[-4000:])
    text = subprocess.check_output(
        ["pdftotext", str(path.with_suffix(".pdf")), "-"], text=True,
    )
    for french, english in HEADINGS.values():
        assert french in text and english in text, (document_class, french, english)
    aux = path.with_suffix(".aux").read_text()
    labels = dict(re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]+)\}", aux))
    expected = ("1.1", "1.2", "1.3") if document_class == "article" else ("1", "2", "3")
    assert tuple(labels[name] for name in ("theoremfr", "theoremen", "theorem")) == expected
    default = "Théorème" if document_class == "article" else "Theorem"
    assert f"{default} {expected[2]} (Optional title)" in text
    assert "PARAMETERS: N,b,N-b" in path.with_suffix(".log").read_text()
    print(f"{document_class}: bilingual headings, optional titles, counters, scope, and notation passed.")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="shared-macros-") as temporary:
        for document_class in ("article", "llncs"):
            check(document_class, Path(temporary))
