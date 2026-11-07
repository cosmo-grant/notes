#!/bin/sh
# Fail if the committed docs/ differs from a fresh build of the committed notes/.

set -eu

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

git archive HEAD | tar -x -C "$tmp"
mv "$tmp/docs" "$tmp/docs.committed"
uv run --quiet "$tmp/scripts/build.py"

if ! diff -r --brief "$tmp/docs.committed" "$tmp/docs"; then
    echo "docs/ is out of date. Run 'make build' and commit docs/." >&2
    exit 1
fi
