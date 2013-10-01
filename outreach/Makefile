
sheets.pdf: recipes.yam code.pdf
	${HOME}/pi-gate/bin/yam2html -aF
	wkhtmltopdf recipes.html recipes.pdf
	pdfjoin --rotateoversize 'false' --outfile sheets.pdf \
          recipes.pdf jelly-page1.pdf traffic-lights.pdf
code.pdf: code.yam
	${HOME}/pi-gate/bin/yam2html code.yam
	wkhtmltopdf code.html code.pdf
