"""Measure the design PNGs in dp. Used to build the design tokens and every screen.

Scale (see docs/DESIGN_TOKENS.md): the phone frame's grey outline is centred on x = 61.3 and
x = 768.3, so the screen is 707 px = 360 dp wide and 1 dp = 1.964 px. Coordinates printed by this
tool are dp from the top-left corner of the screen (x 62, y 89 in the PNG). Screen 14's frame
has its grey outline drawn 17 px left and 8 px up, but its content sits exactly where every
other screen's does (its tab divider runs past the outline), so it uses the same origin.

Commands (run from the project root, all coordinates in dp):

  python tools/px.py row  <screen> <y> [x0 x1]   colour runs along a horizontal line
  python tools/px.py col  <screen> <x> [y0 y1]   colour runs along a vertical line
  python tools/px.py top  <screen> <x0> <y0> <x1> <y1> [n]   most frequent colours in a box
  python tools/px.py raw  <screen> <x> <y0> <y1> every pixel down a line (1-px borders)
  python tools/px.py at   <screen> <x> <y>       colour of one point
  python tools/px.py bbox <screen> <x0> <y0> <x1> <y1> <hex> [tol]
                                                 bounding box of pixels close to a colour
  python tools/px.py crop <screen> <x0> <y0> <x1> <y1> <out.png> [zoom]

A "run" is a stretch of pixels whose colour stays within a small tolerance of its start;
anti-aliased edge pixels show up as short runs and are skipped (minimum 2 px).
"""
import sys

import numpy as np
from PIL import Image

S = "design/screens/screen-%02d.png"
PX_PER_DP = 707 / 360.0  # 1.964 px per dp
ORIGIN = (62.0, 89.0)  # PNG pixel of the screen's top-left corner
OFFSET = {}  # per-screen (dx, dy) PNG px corrections; none needed (see screen 14 note above)


def load(n):
    return np.asarray(Image.open(S % n).convert("RGB")).astype(int)


def to_px(n, x, y):
    dx, dy = OFFSET.get(n, (0, 0))
    return ORIGIN[0] + dx + x * PX_PER_DP, ORIGIN[1] + dy + y * PX_PER_DP


def to_dp(n, px, py):
    dx, dy = OFFSET.get(n, (0, 0))
    return (px - ORIGIN[0] - dx) / PX_PER_DP, (py - ORIGIN[1] - dy) / PX_PER_DP


def hexc(c):
    return "#%02X%02X%02X" % tuple(int(v) for v in c)


def runs(line, tol=10, min_len=2):
    """Split a line of RGB pixels into runs of near-constant colour: (start, end, colour)."""
    out = []
    start = 0
    for i in range(1, len(line) + 1):
        if i == len(line) or np.abs(line[i] - line[start]).max() > tol:
            if i - start >= min_len:
                seg = line[start:i]
                out.append((start, i, np.median(seg, axis=0)))
            start = i
    return out


def main():
    cmd, n = sys.argv[1], int(sys.argv[2])
    a = load(n)
    args = [float(v) for v in sys.argv[3:] if not v.startswith("#") and not v.endswith(".png")]
    if cmd in ("row", "col"):
        pos = args[0]
        lo, hi = (args[1], args[2]) if len(args) >= 3 else (0, 360 if cmd == "row" else 778)
        if cmd == "row":
            _, py = to_px(n, 0, pos)
            x0, _ = to_px(n, lo, 0)
            x1, _ = to_px(n, hi, 0)
            line = a[int(round(py)), int(round(x0)):int(round(x1))]
            base = x0
        else:
            px, _ = to_px(n, pos, 0)
            _, y0 = to_px(n, 0, lo)
            _, y1 = to_px(n, 0, hi)
            line = a[int(round(y0)):int(round(y1)), int(round(px))]
            base = y0
        for s, e, c in runs(line):
            d0 = (base + s - (ORIGIN[0] + OFFSET.get(n, (0, 0))[0] if cmd == "row"
                              else ORIGIN[1] + OFFSET.get(n, (0, 0))[1])) / PX_PER_DP
            print("%7.1f - %7.1f dp  (%5.1f dp, %3d px)  %s" % (d0, d0 + (e - s) / PX_PER_DP,
                                                              (e - s) / PX_PER_DP, e - s, hexc(c)))
    elif cmd == "top":
        x0, y0 = to_px(n, args[0], args[1])
        x1, y1 = to_px(n, args[2], args[3])
        k = int(args[4]) if len(args) > 4 else 8
        box = a[int(y0):int(y1), int(x0):int(x1)].reshape(-1, 3)
        cols, counts = np.unique(box, axis=0, return_counts=True)
        order = np.argsort(-counts)[:k]
        for i in order:
            print("%s  %5.1f%%" % (hexc(cols[i]), 100.0 * counts[i] / len(box)))
    elif cmd == "raw":
        # Every PNG pixel down a vertical line, for 1-px borders that "col" skips.
        px_, _ = to_px(n, args[0], 0)
        _, y0 = to_px(n, 0, args[1])
        _, y1 = to_px(n, 0, args[2])
        for yy in range(int(round(y0)), int(round(y1))):
            print("%7.2f dp  %s" % (to_dp(n, 0, yy)[1], hexc(a[yy, int(round(px_))])))
    elif cmd == "at":
        px, py = to_px(n, args[0], args[1])
        print(hexc(a[int(round(py)), int(round(px))]))
    elif cmd == "bbox":
        target = np.array([int(sys.argv[7][i:i + 2], 16) for i in (1, 3, 5)])
        tol = args[4] if len(args) > 4 else 24
        x0, y0 = to_px(n, args[0], args[1])
        x1, y1 = to_px(n, args[2], args[3])
        box = a[int(y0):int(y1), int(x0):int(x1)]
        m = np.abs(box - target).max(axis=2) <= tol
        ys, xs = np.where(m)
        if len(xs) == 0:
            print("no match")
            return
        bx0, by0 = to_dp(n, xs.min() + int(x0), ys.min() + int(y0))
        bx1, by1 = to_dp(n, xs.max() + 1 + int(x0), ys.max() + 1 + int(y0))
        print("x %.1f - %.1f  y %.1f - %.1f   size %.1f x %.1f dp" %
              (bx0, bx1, by0, by1, bx1 - bx0, by1 - by0))
    elif cmd == "crop":
        out = [v for v in sys.argv[3:] if v.endswith(".png")][0]
        zoom = int(args[4]) if len(args) > 4 else 4
        x0, y0 = to_px(n, args[0], args[1])
        x1, y1 = to_px(n, args[2], args[3])
        img = Image.open(S % n).convert("RGB").crop((int(x0), int(y0), int(x1), int(y1)))
        img.resize((img.width * zoom, img.height * zoom), Image.NEAREST).save(out)
        print("saved", out)


if __name__ == "__main__":
    main()
