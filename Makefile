# make run file=proposal
# make clear file=proposal

DOCNAME=$(file)

run: 
	pdflatex $(DOCNAME).tex
	biber $(DOCNAME)
	pdflatex $(DOCNAME).tex
	pdflatex $(DOCNAME).tex

# for Windows
clear:
	del $(DOCNAME).aux
	del $(DOCNAME).bbl
	del $(DOCNAME).bcf
	del $(DOCNAME).blg
	del $(DOCNAME).lof
	del $(DOCNAME).log
	del $(DOCNAME).lot
	del $(DOCNAME).out
	del $(DOCNAME).run.xml
	del $(DOCNAME).toc
	del $(DOCNAME).apc
