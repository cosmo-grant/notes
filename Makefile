.PHONY: view publish preview

view:
	open "https://cosmo-grant.github.io/notes"

preview:
	asciidoctor --destination-dir preview/ --attribute source-highlighter=highlightjs --attribute highlightjs-theme=monokai drafts/*.adoc
	uv run scripts/make_index.py preview
	open "./preview/index.html"

publish:
	asciidoctor --destination-dir docs/ --attribute source-highlighter=highlightjs --attribute highlightjs-theme=monokai drafts/*.adoc
	uv run scripts/make_index.py docs
