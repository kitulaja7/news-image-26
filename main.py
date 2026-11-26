#!/usr/bin/env python3
"""news-image-20261126 entry point (standard library only).

Copies the committed entry.png to the output directory byte-for-byte.
The image itself is rendered at dev time by render.py (PIL); this program
does no drawing and needs no network, so it runs identically twice.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(OUT_DIR, "entry.png"))


if __name__ == "__main__":
    main()
