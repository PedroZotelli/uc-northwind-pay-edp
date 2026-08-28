#!/usr/bin/env python3
"""assemble.py — pack shots/p*.jpg into ebooks/ebook-converge.pdf at exactly 1440x900 pt."""
import glob
import os
import subprocess
import sys

import img2pdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ebooks/.build
SHOTS = os.path.join(ROOT, "shots")
OUT = os.path.normpath(os.path.join(ROOT, "..", "ebook-converge.pdf"))

pages = sorted(glob.glob(os.path.join(SHOTS, "p*.jpg")))
if not pages:
    sys.exit("assemble: no shots/p*.jpg found")

layout = img2pdf.get_fixed_dpi_layout_fun((108, 108))  # 2160x1350 px @108dpi -> 1440x900 pt
with open(OUT, "wb") as f:
    f.write(img2pdf.convert(pages, layout_fun=layout))

info = subprocess.run(["pdfinfo", OUT], capture_output=True, text=True).stdout
npages = next((l.split()[-1] for l in info.splitlines() if l.startswith("Pages")), "?")
size = next((l.split(":", 1)[1].strip() for l in info.splitlines() if l.startswith("Page size")), "?")
print(f"assemble: {OUT}")
print(f"assemble: {len(pages)} shots -> Pages: {npages} | Page size: {size}")
if str(npages) != str(len(pages)) or "1440 x 900" not in size:
    sys.exit("assemble: page count or size mismatch")
