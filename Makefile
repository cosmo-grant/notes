.PHONY: view publish

publish:
	asciidoctor --destination-dir docs/ --attribute source-highlighter=highlightjs --attribute highlightjs-theme=monokai --attribute nofooter notes/*.adoc
	uv run scripts/make_index.py
	xdg-open "docs/index.html"

view:
	open "https://cosmo-grant.github.io/notes"
