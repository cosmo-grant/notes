# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

"""
Build the site from notes/.

Published posts (those with a :published: date) go to docs/.
With --preview, drafts are included too and output goes to preview/.
"""

import argparse
import shutil
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).parent.parent
NOTES_DIR = ROOT / "notes"
TEMPLATES_DIR = ROOT / "templates"
INDEX_TEMPLATE = TEMPLATES_DIR / "index.adoc"

SITE_URL = "https://cosmo-grant.github.io/notes/"
SITE_TITLE = "Notes"
AUTHOR = "Cosmo Grant"

ASCIIDOCTOR_ATTRIBUTES = [
    "source-highlighter=highlightjs",
    "highlightjs-theme=monokai",
    "nofooter",
    "linkcss",
    "copycss",
    "docinfo=shared",
    f"docinfodir={TEMPLATES_DIR}",
]


@dataclass
class Post:
    path: Path
    title: str
    published: date | None

    @property
    def filename(self) -> str:
        return self.path.stem + ".html"


def parse_header(path: Path) -> Post:
    title = None
    published = None
    for line in path.read_text().splitlines():
        if not line.strip():
            break
        if line.startswith("= "):
            title = line.removeprefix("= ").strip()
        elif line.startswith(":published:"):
            published = date.fromisoformat(line.removeprefix(":published:").strip())
    if title is None:
        raise ValueError(f"{path}: no title")
    return Post(path, title, published)


def asciidoctor(out_dir: Path, *args, input: str | None = None) -> None:
    attributes = [arg for attribute in ASCIIDOCTOR_ATTRIBUTES for arg in ("--attribute", attribute)]
    subprocess.run(
        ["asciidoctor", "--destination-dir", out_dir, *attributes, *args],
        input=input,
        text=True,
        check=True,
    )


def render_index(posts: list[Post]) -> str:
    lines = [INDEX_TEMPLATE.read_text().rstrip(), ""]
    for post in posts:
        label = post.published.isoformat() if post.published else "draft"
        title = post.title.replace("]", r"\]")
        lines.append(f"* {label} link:{post.filename}[{title}]")
    return "\n".join(lines) + "\n"


def render_feed(posts: list[Post]) -> str:
    published = [post for post in posts if post.published]
    updated = max(post.published for post in published)
    entries = "".join(
        f"""
  <entry>
    <title>{escape(post.title)}</title>
    <link href="{SITE_URL}{post.filename}"/>
    <id>{SITE_URL}{post.filename}</id>
    <published>{post.published}T00:00:00Z</published>
    <updated>{post.published}T00:00:00Z</updated>
  </entry>"""
        for post in published
    )
    return f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{SITE_TITLE}</title>
  <link href="{SITE_URL}"/>
  <link rel="self" href="{SITE_URL}feed.xml"/>
  <id>{SITE_URL}</id>
  <updated>{updated}T00:00:00Z</updated>
  <author><name>{AUTHOR}</name></author>{entries}
</feed>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview", action="store_true", help="include drafts; output to preview/")
    args = parser.parse_args()

    out_dir = ROOT / ("preview" if args.preview else "docs")
    posts = [parse_header(path) for path in NOTES_DIR.glob("*.adoc")]
    if not args.preview:
        posts = [post for post in posts if post.published]
    posts.sort(key=lambda post: post.published or date.max, reverse=True)

    shutil.rmtree(out_dir, ignore_errors=True)
    asciidoctor(out_dir, *(post.path for post in posts))
    shutil.copytree(NOTES_DIR / "images", out_dir / "images")
    asciidoctor(out_dir, "--out-file", "index.html", "-", input=render_index(posts))
    (out_dir / "feed.xml").write_text(render_feed(posts))


if __name__ == "__main__":
    main()
