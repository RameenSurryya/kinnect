"""Compare the ph_<family>.xml placeholders with every frame in the design PNGs.

For every frame listed in design/check/placeholder_geometry.json the drawable is rendered like
ImageView scaleType="centerCrop" (scaled to cover the frame, centred, the rest cut off) and
compared pixel by pixel with the design. One sheet per family is saved to design/check/ph_<family>.png:

    design crop | my drawable, centre-cropped | overlay

Overlay: grey = same layer in both, red = the design has a higher layer there (my shape is too
small or too low), blue = mine has a higher layer (my shape is too big or too high), white =
ignored (text, buttons, anti-aliased edges in the design).
Layers, low to high: sky, sun, back hill, front hill.

Run from the project root:  python tools/check_placeholders.py   (needs pillow, pymupdf, numpy)
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from check_glyphs import render_drawable  # noqa: E402  (VectorDrawable -> image, same renderer)
from sample_placeholders import ROLES, label  # noqa: E402

S = "design/screens/screen-%02d.png"
OUT = "design/check/ph_%s.png"
ROW_H = 200  # height of one row in the sheet


def centre_crop(name, W, H):
    """Render the square drawable big enough to cover W x H and cut out the middle."""
    side = max(W, H)
    img = render_drawable(name, side).convert("RGB")
    left, top = (side - W) // 2, (side - H) // 2
    return img.crop((left, top, left + W, top + H))


def main():
    g = json.load(open("design/check/placeholder_geometry.json"))
    pal = {f: {r: np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)]) for r, c in cols.items()}
           for f, cols in g["colours"].items()}
    by_fam = {}
    for fr in g["frames"]:
        by_fam.setdefault(fr["fam"], []).append(fr)

    total = []
    for fam, frames in by_fam.items():
        rows = []
        for fr in frames:
            x0, y0, x1, y1 = fr["box"]
            W, H = x1 - x0, y1 - y0
            design = Image.open(S % fr["screen"]).convert("RGB").crop((x0, y0, x1, y1))
            mine = centre_crop("ph_" + fam, W, H)
            ld = label(np.asarray(design), pal[fam])
            if fr.get("scrim"):
                ld[fr["scrim"] - y0:] = -1  # dark name scrim in 04's story cards: ignore
            lm = label(np.asarray(mine), pal[fam], tol=60)
            known = (ld >= 0) & (lm >= 0)
            diff = known & (ld != lm)
            # mismatched pixels per curve-length: roughly the mean edge offset in design px
            offset = diff.sum() / (2 * W)
            total.append(offset)
            ov = np.full((H, W, 3), 255, np.uint8)
            ov[known & ~diff] = (190, 190, 190)
            ov[diff & (ld > lm)] = (220, 40, 40)
            ov[diff & (ld < lm)] = (40, 90, 230)
            rows.append((fr, design, mine, Image.fromarray(ov), offset, 100 * diff.sum() / known.sum()))
            print(f"{fam:6s} s{fr['screen']:02d} {W}x{H}  mismatch {rows[-1][5]:5.2f}% of pixels, "
                  f"mean edge offset {offset:.2f}px")

        # sheet: one row per frame, scaled to ROW_H high (wide frames capped at 3 * ROW_H)
        scaled = []
        for fr, d, m, o, off, pct in rows:
            w, h = d.size
            k = min(ROW_H / h, 3 * ROW_H / w)
            size = (max(1, round(w * k)), max(1, round(h * k)))
            scaled.append(([p.resize(size, Image.LANCZOS if p is not o else Image.NEAREST)
                            for p in (d, m, o)], fr, off, pct))
        sheet_w = max(3 * p[0][0].width for p in scaled) + 40
        sheet_h = sum(p[0][0].height + 24 for p in scaled) + 10
        sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
        dr = ImageDraw.Draw(sheet)
        y = 5
        for panels, fr, off, pct in scaled:
            dr.text((10, y), f"ph_{fam}  screen {fr['screen']:02d}  box {fr['box']}   design | mine "
                             f"(centerCrop) | overlay red=design higher, blue=mine higher   "
                             f"mismatch {pct:.2f}%  edge offset {off:.2f}px", fill="black")
            for i, p in enumerate(panels):
                sheet.paste(p, (10 + i * (p.width + 10), y + 18))
            y += panels[0].height + 24
        sheet.save(OUT % fam, optimize=True)
    print(f"mean edge offset over all frames: {np.mean(total):.2f}px")


if __name__ == "__main__":
    main()
