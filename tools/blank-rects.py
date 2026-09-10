#!/usr/bin/env python3
"""Report declared atlas rects that draw nothing.

A fully transparent rect passes every check the build already makes: it is in
bounds, non-zero-sized, uniquely positioned, and carries real provenance. It
just paints no pixels. See docs/audits/FINDING_blank_rects.md.

    python3 tools/blank-rects.py [aetherfall.html]

Needs Pillow.
"""
import re, sys, io, base64
from PIL import Image

build = sys.argv[1] if len(sys.argv) > 1 else "aetherfall.html"
src = open(build).read()
blk = src[src.index("const RECTS = {"):]
blk = blk[:blk.index("\n  };")]
rects = {m.group(1): tuple(map(int, m.group(2).split(",")))
         for m in re.finditer(r'"([A-Za-z0-9_]+)":\[([0-9,]+)\]', blk)}
uris = re.findall(r'data:image/(?:png|webp);base64,([A-Za-z0-9+/=]+)', src)
atlas = Image.open(io.BytesIO(base64.b64decode(max(uris, key=len)))).convert("RGBA")

blank, faint = [], []
for k, (x, y, w, h) in sorted(rects.items()):
    a = atlas.crop((x, y, x + w, y + h)).getchannel("A")
    n = sum(1 for p in a.get_flattened_data() if p)
    if n == 0:
        blank.append((k, x, y, w, h))
    elif n * 100 < w * h:          # under 1% ink — worth a human glance
        faint.append((k, n, w * h))

print(f"{len(rects)} rects checked")
print(f"\nFULLY TRANSPARENT — declared, drawn, and invisible: {len(blank)}")
for k, x, y, w, h in blank:
    print(f"   {k:24} {x},{y} {w}x{h}")
print(f"\nunder 1% ink (not necessarily wrong): {len(faint)}")
for k, n, tot in faint:
    print(f"   {k:24} {n}/{tot} opaque")
sys.exit(1 if blank else 0)
