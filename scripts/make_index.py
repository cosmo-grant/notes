# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "jinja2",
# ]
# ///


from argparse import ArgumentParser
from pathlib import Path
import subprocess

from jinja2 import Environment, FileSystemLoader

def get_display_name(note):
    return note.stem.replace("_", " ")


def main():
    parser = ArgumentParser()
    parser.add_argument("target", choices=["docs", "preview"])
    args = parser.parse_args()
    target = Path(__file__).parent.parent / args.target

    env = Environment(loader=FileSystemLoader("templates/"))
    index_template = env.get_template("index.adoc.jinja")

    notes = [note for note in target.iterdir() if note.name != "index.html"]
    rendered_adoc = index_template.render(
        notes=[(note.name, get_display_name(note)) for note in notes]
    )

    subprocess.run(["asciidoctor", "--destination-dir", target, "--out-file", "index.html", "--attribute", "nofooter", "-"], text=True, input=rendered_adoc, check=True)


if __name__ == "__main__":
    main()
