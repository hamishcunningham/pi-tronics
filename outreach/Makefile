
sheets.pdf: recipes.yam code.pdf
	yam2html -a
	wkhtmltopdf recipes.html recipes.pdf
	pdfjoin --rotateoversize 'false' --outfile sheets.pdf \
          recipes.pdf jelly-page1.pdf traffic-page1.pdf code.pdf
code.pdf: code.yam
	${HOME}/pi-gate/bin/yam2html code.yam
	wkhtmltopdf code.html code.pdf
