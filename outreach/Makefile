
sheets.pdf: recipes.yam
	yam2html -a
	wkhtmltopdf recipes.html recipes.pdf
	pdfjoin --rotateoversize 'false' --outfile sheets.pdf \
          recipes.pdf jelly-page1.pdf traffic-page1.pdf
