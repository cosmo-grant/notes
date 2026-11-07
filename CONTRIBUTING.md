# Contributing

Requires asciidoctor, uv and pre-commit.

```sh
pre-commit install
```

## Write

Posts are AsciiDoc files in `notes/`.
Every post starts with a title:

```adoc
= My title
```

A post without a `:published:` date is a draft.

Images go in `notes/images/`:

```adoc
image::./images/foo.png[Alt text]
```

## Preview

```sh
make preview
```

This serves drafts and published posts at http://localhost:8000.
After editing, run `uv run scripts/build.py --preview` and refresh.

## Publish

Add the date under the title:

```adoc
= My title
:published: 2026-11-07
```

Then `make build`, commit and push.
The pre-push hook fails if `docs/` is out of date.

The filename is the URL, so don't rename published posts.
Editing a published post doesn't change the feed.
