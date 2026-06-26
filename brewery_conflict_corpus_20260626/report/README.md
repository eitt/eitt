# Preliminary LaTeX Report

This folder contains an Overleaf-ready preliminary scientific report:

- `brewery_conflict_preliminary_report.tex`

Compile in Overleaf or locally with:

```bash
pdflatex brewery_conflict_preliminary_report.tex
bibtex brewery_conflict_preliminary_report
pdflatex brewery_conflict_preliminary_report.tex
pdflatex brewery_conflict_preliminary_report.tex
```

The report uses an APA-style manuscript layout via the `apa7` class and `apacite`. It references the shared bibliography at `../bibliography/references.bib` and does not include generated binary outputs.
