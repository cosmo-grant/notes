.PHONY: publish preview

html:
	asciidoctor -D preview/ -a source-highlighter=highlightjs -a highlightjs-theme=monokai drafts/*.adoc

publish:
	asciidoctor -D docs/ -a source-highlighter=highlightjs -a highlightjs-theme=monokai drafts/$(FILE)

view:
	open "https://cosmo-grant.github.io/notes"

preview:
	open "./preview/index.html"
