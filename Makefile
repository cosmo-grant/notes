.PHONY: build preview view

build:
	uv run scripts/build.py

preview:
	uv run scripts/build.py --preview
	python3 -m http.server --bind 127.0.0.1 --directory preview

view:
	xdg-open "https://cosmo-grant.github.io/notes"
