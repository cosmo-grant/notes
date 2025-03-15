html-all:
  asciidoctor -D html/ *.adoc

html ADOC_FILENAME:
  asciidoctor -D html/ "{{ADOC_FILENAME}}"

publish:
  asciidoctor -D public/ *.adoc

refresh-index:
  echo not implemented
