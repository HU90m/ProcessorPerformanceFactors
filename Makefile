CONTENT=$(shell ls content | sed 's/.md/.tex/;s/^/content-/')

report.pdf: report.tex $(CONTENT)
	echo "" | pdflatex report
	echo "" | pdflatex report
	echo "" | pdflatex report
	@#pdftotext -layout report.pdf 


content-%.tex: content/%.md
	echo "" | pandoc -t latex $< -o $@

clean:
	rm -f report.pdf *.log *.aux *.backup *.out content-*.tex *.bbl *.bcf *.blg *.run.xml *.fdb_latexmk *.fls *.toc *.synctex.gz *.glo *.glg *.gls *.ist *.txt