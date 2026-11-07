PYTHON ?= python

.PHONY: readme json fetch

readme:
	$(PYTHON) tools/render_readme.py

json:
	$(PYTHON) tools/render_json.py

fetch:
	$(PYTHON) tools/fetch_repos.py
