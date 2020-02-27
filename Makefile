CONTENT=$(shell ls content | sed 's/.md/.tex/;s/^/content-/')

report.pdf: report.tex refs.bib $(CONTENT)
	echo "" | pdflatex report
	echo "" | bibtex report 
	echo "" | pdflatex report
	echo "" | pdflatex report
	@#pdftotext -layout report.pdf 

clean:
	rm -f report.pdf *.log *.aux *.backup *.out content-*.tex *.bbl *.bcf *.blg *.run.xml *.fdb_latexmk *.fls *.toc *.synctex.gz *.glo *.glg *.gls *.ist *.txt