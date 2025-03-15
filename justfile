html-all:
  asciidoctor -D html/ *.adoc

html ADOC_FILENAME:
  asciidoctor -D html/ "{{ADOC_FILENAME}}"

publish:
  asciidoctor -D public/ *.adoc

refresh-index:
  #!/usr/bin/env sh
  BASE_URL="https://cosmo-grant.github.io/notes"
  echo "== Notes\n" >index.adoc
  for NOTE in *.adoc; do
    if [ $NOTE = index.adoc ]; then
      continue
    fi
    NOTE_WITHOUT_EXTENSION=$(basename $NOTE .adoc)
    TITLE=$(echo ${NOTE_WITHOUT_EXTENSION} | tr '_' ' ')
    echo "* ${BASE_URL}/${NOTE_WITHOUT_EXTENSION}.html[$TITLE]" >>index.adoc
  done
