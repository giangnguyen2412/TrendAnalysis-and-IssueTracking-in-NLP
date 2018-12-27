.PHONY: doc


doc:
	rm -rf doc
	mkdir -p doc
	pydoc3 -w `find -type f -iname "*.py" -execdir basename {} .py ';'`
	mv *.html doc
	python3 postprocess_html.py
