"""Write the ph_<family>.xml photo placeholder VectorDrawables.

Reads design/check/placeholder_geometry.json (made by tools/sample_placeholders.py), fits each
hill outline with a chain of smooth cubic Bezier curves, and writes one drawable per colour
family to app/src/main/res/drawable. All seven drawables share the same shapes; only the four
colours change.

The design shows every placeholder as a centre crop of one square picture, so the viewport is
square (360 x 360) and ImageViews must use android:scaleType="centerCrop".

Run from the project root:  python tools/make_placeholders.py   (needs numpy, scipy)
"""
import json

import numpy as np
from scipy.optimize import least_squares

GEOM = "design/check/placeholder_geometry.json"
OUT = "app/src/main/res/drawable/ph_%s.xml"
V = 360  # viewport size (square)
# Knots of each hill outline: "end" = picture edge (may sit just outside, free tangent),
# "flat" = crest or trough (horizontal tangent, like a designer's pen tool), "free" = extra knot
# with a free tangent. An extra knot on the front hill (it steepens in the last 15 units) was
# tried: the fit improves but nothing changes in any design frame, so both hills use 3 curves.
KNOTS = {"back": ("end", "flat", "flat", "end"),
         "front": ("end", "flat", "flat", "end")}


def bezier(p0, p1, p2, p3, t):
    t = t[:, None]
    return ((1 - t) ** 3) * p0 + 3 * ((1 - t) ** 2) * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3


def unpack(q, kinds):
    """Parameters -> list of segments (p0, p1, p2, p3).
    q = knot y's, knot x's, tangent angles of the non-flat knots, two handle lengths per segment.
    Each knot has one tangent direction, so the outline is smooth everywhere."""
    k = len(kinds)
    n = k - 1
    ys, xs = q[:k], q[k:2 * k]
    free = iter(q[2 * k:])
    ang = [0.0 if kind == "flat" else next(free) for kind in kinds]
    ln = q[-2 * n:].reshape(n, 2)
    segs = []
    for i in range(n):
        p0 = np.array([xs[i], ys[i]])
        p3 = np.array([xs[i + 1], ys[i + 1]])
        d0 = np.array([np.cos(ang[i]), np.sin(ang[i])])
        d1 = np.array([np.cos(ang[i + 1]), np.sin(ang[i + 1])])
        segs.append((p0, p0 + ln[i, 0] * d0, p3 - ln[i, 1] * d1, p3))
    return segs


def sample(segs, k=200):
    return np.concatenate([bezier(*s, np.linspace(0, 1, k)) for s in segs])


def residual(q, kinds, x, y):
    pts = sample(unpack(q, kinds))
    order = np.argsort(pts[:, 0])
    return np.interp(x, pts[order, 0], pts[order, 1]) - y


def fit(curve, kinds):
    x, y = np.array(curve).T * V
    # start: crest and trough at the highest and lowest measured points, an extra knot halfway
    # between the trough and the right edge, handles a third of the segment
    crest, trough = x[np.argmin(y)], x[np.argmax(y)]
    kx = np.array([0, crest, trough] + ([(trough + V) / 2] if len(kinds) == 5 else []) + [V], float)
    k, n, nfree = len(kinds), len(kinds) - 1, sum(kind != "flat" for kind in kinds)
    span = np.diff(kx).mean()
    q0 = np.r_[np.interp(kx, x, y), kx + np.r_[-1, np.zeros(k - 2), 1], np.zeros(nfree),
               np.full(2 * n, span / 3)]
    # knot x limits: ends just outside the picture, inner knots within 40 units of the start
    xlo = np.r_[-60, kx[1:-1] - 40, V]
    xhi = np.r_[0, kx[1:-1] + 40, V + 60]
    lo = np.r_[np.zeros(k), xlo, np.full(nfree, -1.5), np.ones(2 * n)]
    hi = np.r_[np.full(k, V), xhi, np.full(nfree, 1.5), np.full(2 * n, V / 2)]
    r = least_squares(residual, q0, bounds=(lo, hi), args=(kinds, x, y))
    err = np.abs(r.fun)
    print(f"      worst points (x, error): " + ", ".join(
        f"({x[i]:.0f}, {r.fun[i]:+.2f})" for i in np.argsort(-err)[:5]))
    return unpack(r.x, kinds), err.mean(), err.max()


def path(segs):
    """Hill outline left to right, then down to the bottom corners and closed."""
    f = lambda p: f"{p[0]:.1f},{p[1]:.1f}"
    d = f"M{f(segs[0][0])}"
    for _, c1, c2, p in segs:
        d += f" C{f(c1)} {f(c2)} {f(p)}"
    return d + f" L{segs[-1][3][0]:.1f},{V} L{segs[0][0][0]:.1f},{V} Z"


TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<!-- Photo placeholder "{fam}": flat sky, pale sun and two wavy hills, copied from the design
     (sampled colours, shapes measured by tools/sample_placeholders.py, written by
     tools/make_placeholders.py). The viewport is square because every placeholder in the
     design is a centre crop of the same square picture: use android:scaleType="centerCrop". -->
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="360dp"
    android:height="360dp"
    android:viewportWidth="{V}"
    android:viewportHeight="{V}">

    <!-- sky -->
    <path
        android:fillColor="{bg}"
        android:pathData="M0,0 L{V},0 L{V},{V} L0,{V} Z" />

    <!-- sun: circle at ({cx:.1f}, {cy:.1f}), radius {r:.1f}, drawn as two half arcs -->
    <path
        android:fillColor="{sun}"
        android:pathData="M{sx0:.1f},{cy:.1f} A{r:.1f},{r:.1f} 0 1,1 {sx1:.1f},{cy:.1f} A{r:.1f},{r:.1f} 0 1,1 {sx0:.1f},{cy:.1f} Z" />

    <!-- back hill (lighter): high on the left, dips on the right -->
    <path
        android:fillColor="{back}"
        android:pathData="{back_d}" />

    <!-- front hill (darker), drawn over the back hill -->
    <path
        android:fillColor="{front}"
        android:pathData="{front_d}" />
</vector>
"""


def main():
    g = json.load(open(GEOM))
    cx, cy, r = g["sun"][0] * V, g["sun"][1] * V, g["sun"][2] * V
    paths = {}
    for k in ("back", "front"):
        segs, mean, mx = fit(g["curves"][k], KNOTS[k])
        paths[k] = path(segs)
        print(f"{k:5s} fit error: mean {mean:.2f}, max {mx:.2f} viewport units   {paths[k]}")
    print(f"sun   centre ({cx:.1f}, {cy:.1f}) radius {r:.1f}")
    for fam, c in g["colours"].items():
        xml = TEMPLATE.format(fam=fam, V=V, cx=cx, cy=cy, r=r, sx0=cx - r, sx1=cx + r,
                              back_d=paths["back"], front_d=paths["front"], **c)
        open(OUT % fam, "w", newline="\n").write(xml)
        print("wrote", OUT % fam)


if __name__ == "__main__":
    main()
