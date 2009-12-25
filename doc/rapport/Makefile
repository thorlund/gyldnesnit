all: pdf

pdf: rapport.tex litteraturliste.bib afsnit/*
	pdflatex rapport.tex
	bibtex rapport
	pdflatex rapport.tex
	pdflatex rapport.tex

test: test.tex litteraturliste.bib afsnit/*
	pdflatex test.tex
	bibtex test
	pdflatex test.tex
	pdflatex test.tex
	mv -f test.pdf rapport.pdf
