"""Copy the finished front-page image to the output directory.

Entry point for the news-image-20261119 contest. The image itself is
drawn ahead of time by tools/render.py and stored at assets/entry.png;
this program only places that exact file at the path the contest
harness expects. It does no network, keeps no time, and makes no
random choice, so running it twice writes the same bytes twice.

Usage: python3 main.py
Output: <MAKEFUN_OUTPUT_DIR or /output>/entry.png
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "assets" / SOURCE_NAME
    if not source.is_file():
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, out_dir / OUTPUT_NAME)
    print(f"wrote {out_dir / OUTPUT_NAME}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
