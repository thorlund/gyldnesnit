all: pdf gennemsyn

pdf: rapport.tex litteraturliste.bib afsnit/*
	pdflatex rapport.tex
	bibtex rapport
	pdflatex rapport.tex
	pdflatex rapport.tex

gennemsyn: gennemsyn.tex litteraturliste.bib afsnit/*
	pdflatex gennemsyn.tex
	bibtex gennemsyn
	pdflatex gennemsyn.tex
	pdflatex gennemsyn.tex
