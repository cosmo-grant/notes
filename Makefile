.PHONY: view publish

view:
	open "https://cosmo-grant.github.io/notes"

publish:
	asciidoctor --destination-dir docs/ --attribute source-highlighter=highlightjs --attribute highlightjs-theme=monokai --attribute nofooter notes/*.adoc
	uv run scripts/make_index.py
	open "docs/index.html"
