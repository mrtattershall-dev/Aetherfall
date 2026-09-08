#!/usr/bin/env python3
"""Parse the build's RECTS table and decode its embedded atlas, then check the
two things a self-test inside the build cannot check cheaply from outside:
that every rect is real, and that no two ids point at the same picture.

    python3 tools/atlas-report.py [aetherfall.html]

Needs Pillow. Prints rect count, integrity, and the packed extent against the
declared atlas size. Optionally dumps the atlas with --save-atlas PATH so an
audit can compare frames pixel-for-pixel against the source packs — the check
AUDIT_0_9_3 records as "cannot become a self-test", because it needs archives
the build does not ship.
"""
import re, sys, io, base64, argparse
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("build", nargs="?", default="aetherfall.html")
ap.add_argument("--save-atlas", metavar="PATH")
a = ap.parse_args()

src = open(a.build).read()
blk = src[src.index("const RECTS = {"):]
blk = blk[:blk.index("\n  };")]
rects = {m.group(1): tuple(map(int, m.group(2).split(",")))
         for m in re.finditer(r'"([A-Za-z0-9_]+)":\[([0-9,]+)\]', blk)}

decl = re.search(r'const W = (\d+), H = (\d+)', src)
W, H = (int(decl.group(1)), int(decl.group(2))) if decl else (None, None)

zero = [k for k, (x, y, w, h) in rects.items() if w <= 0 or h <= 0]
oob  = [k for k, (x, y, w, h) in rects.items() if W and (x + w > W or y + h > H)]
dupe = [c for c, n in Counter(rects.values()).items() if n > 1]
mx = max(x + w for x, y, w, h in rects.values())
my = max(y + h for x, y, w, h in rects.values())

print(f"rects            {len(rects)}")
print(f"declared atlas   {W}x{H}")
print(f"packed extent    {mx}x{my}")
print(f"zero-sized       {len(zero)} {zero or ''}")
print(f"out of bounds    {len(oob)} {oob or ''}")
print(f"duplicate coords {len(dupe)}   (two ids drawing the same picture)")

if a.save_atlas:
    from PIL import Image
    uris = re.findall(r'data:image/(?:png|webp);base64,([A-Za-z0-9+/=]+)', src)
    img = Image.open(io.BytesIO(base64.b64decode(max(uris, key=len))))
    img.save(a.save_atlas)
    print(f"atlas written    {a.save_atlas} {img.size}")
