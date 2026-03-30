# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "jinja2",
# ]
# ///

"""
Create an index.html from the notes in docs/.
"""

from pathlib import Path
import subprocess

from jinja2 import Environment, FileSystemLoader


def main():
    env = Environment(loader=FileSystemLoader("templates/"))
    index_template = env.get_template("index.adoc.jinja")
    docs_dir = Path(__file__).parent.parent / "docs"
    notes = [note for note in docs_dir.iterdir() if note.name not in ("index.html", "images")]
    rendered_adoc = index_template.render(notes=[(note.name, note.stem.replace("_", " ")) for note in notes])

    subprocess.run(
        [
            "asciidoctor",
            "--destination-dir",
            docs_dir,
            "--out-file",
            "index.html",
            "--attribute",
            "nofooter",
            "-",
        ],
        input=rendered_adoc,
        text=True,
        check=True,
    )


if __name__ == "__main__":
    main()
