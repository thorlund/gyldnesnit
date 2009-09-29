all: rapport.pdf

rapport.pdf: rapport.tex litteraturliste.bib
	pdflatex rapport.tex
	bibtex rapport
	pdflatex rapport.tex
	pdflatex rapport.tex
