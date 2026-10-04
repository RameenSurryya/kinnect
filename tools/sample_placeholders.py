"""Sample the photo placeholders (flat sun-and-hills illustrations) from the design PNGs.

Every placeholder in the design is the SAME scene (one sun, a back hill, a front hill) in one of
seven colour families, shown through a frame of a different shape. Each frame shows a centre crop
of one master picture, exactly like ImageView scaleType="centerCrop". This script

  1. samples the four flat colours of each family (background, sun, back hill, front hill),
  2. measures the sun outline and both hill outlines in every frame (with sub-pixel edges),
  3. maps every frame back to master coordinates for a range of master aspect ratios and prints
     the one where all frames agree best (0.99: the designer used a square picture), then
     measures everything on an exactly square master, like the square drawable,
  4. writes design/check/placeholder_geometry.json (master curves + sun) and prints a summary.

Run from the project root:  python tools/sample_placeholders.py   (needs pillow, numpy)
"""
import json
from collections import Counter

import numpy as np
from PIL import Image

S = "design/screens/screen-%02d.png"
OUT = "design/check/placeholder_geometry.json"

# One clean frame per family, used to sample the colours (no text or buttons on top).
COLOUR_SOURCE = {
    "sand": (23, (430, 990, 735, 1240)),
    "teal": (4, (425, 995, 765, 1218)),
    "lilac": (17, (316, 1316, 517, 1512)),
    "sky": (23, (98, 935, 405, 1240)),
    "sage": (23, (98, 475, 405, 782)),
    "rose": (23, (430, 475, 735, 782)),
    "night": (17, (97, 1316, 300, 1512)),
}

# Every frame: family, screen, approximate outer box (x0, y0, x1, y1) in PNG pixels.
# Last value: None = find the exact box automatically, or a PNG row = use the box exactly as
# given and ignore everything from that row down (the dark name scrim on 04's story cards).
# 11 gets its box by hand (row 1440 = its bottom edge, nothing ignored): the dark bar under the
# story is close to the night front-hill colour, so the automatic box came out 2 rows too tall.
FRAMES = [
    ("sand", 8, (63, 192, 768, 788), None),
    ("sand", 4, (63, 991, 413, 1459), None),
    ("sand", 23, (424, 928, 739, 1244), None),
    ("sand", 8, (241, 1145, 414, 1318), None),
    ("sand", 8, (595, 1322, 768, 1495), None),
    ("teal", 15, (63, 193, 768, 547), None),
    ("teal", 16, (93, 570, 739, 785), None),
    ("teal", 4, (421, 991, 768, 1220), None),
    ("teal", 8, (241, 791, 414, 965), None),
    ("teal", 8, (595, 968, 768, 1141), None),
    ("lilac", 21, (385, 1112, 746, 1363), None),
    ("lilac", 17, (312, 1312, 520, 1516), None),
    ("lilac", 8, (418, 791, 591, 965), None),
    ("lilac", 8, (63, 1145, 236, 1318), None),
    ("sky", 6, (173, 1063, 496, 1285), None),
    ("sky", 23, (93, 928, 408, 1244), None),
    ("sky", 17, (529, 1312, 739, 1516), None),
    ("sky", 8, (595, 791, 768, 965), None),
    ("sky", 8, (595, 1145, 768, 1318), None),
    ("sky", 8, (418, 1322, 591, 1495), None),
    ("sage", 12, (78, 106, 753, 1440), None),
    ("sage", 9, (78, 106, 753, 1416), None),
    ("sage", 10, (78, 106, 753, 1440), None),
    ("sage", 23, (93, 470, 408, 786), None),
    ("sage", 8, (63, 968, 236, 1141), None),
    ("sage", 8, (418, 1145, 591, 1318), None),
    ("rose", 23, (424, 470, 739, 786), None),
    ("rose", 4, (498, 436, 684, 752), 674),
    ("rose", 8, (241, 968, 414, 1141), None),
    ("rose", 8, (63, 1322, 236, 1495), None),
    ("night", 11, (78, 105, 753, 1440), 1440),
    ("night", 17, (63, 193, 768, 547), None),
    ("night", 4, (296, 436, 482, 752), 674),
    ("night", 17, (93, 1312, 303, 1516), None),
    ("night", 8, (418, 968, 591, 1141), None),
    ("night", 8, (241, 1322, 414, 1495), None),
]

ROLES = ("bg", "sun", "back", "front")


def hexs(c):
    return "#%02X%02X%02X" % tuple(int(v) for v in c)


# ---------- 1. colours ----------

def sample_colours():
    """Four most frequent exact colours of a clean frame, sorted into roles:
    bg = most common in the top rows, sun = lightest of the rest, back = lighter hill,
    front = darker hill."""
    pal = {}
    for fam, (s, box) in COLOUR_SOURCE.items():
        a = np.asarray(Image.open(S % s).convert("RGB").crop(box)).astype(int)
        # the four most frequent colours, skipping near-duplicates (anti-aliased edge pixels)
        top4 = []
        for c, _ in Counter(map(tuple, a.reshape(-1, 3))).most_common(50):
            c = np.array(c)
            if all(np.abs(c - t).sum() > 20 for t in top4):
                top4.append(c)
            if len(top4) == 4:
                break
        top_rows = Counter(map(tuple, a[: a.shape[0] // 10].reshape(-1, 3))).most_common(1)[0][0]
        bg = min(top4, key=lambda c: np.abs(c - np.array(top_rows)).sum())
        rest = sorted([c for c in top4 if c is not bg], key=lambda c: -c.sum())
        pal[fam] = {"bg": bg, "sun": rest[0], "back": rest[1], "front": rest[2]}
    return pal


def label(a, p, tol=12):
    """Per pixel: 0 bg, 1 sun, 2 back hill, 3 front hill, -1 anything else (edges, overlays)."""
    cols = np.stack([p[r] for r in ROLES])
    d = np.abs(a[:, :, None, :].astype(int) - cols[None, None]).sum(-1)
    lab = d.argmin(-1)
    lab[d.min(-1) > tol] = -1
    return lab


# ---------- 2. measuring one frame ----------

def exact_frame(lab, x0, y0):
    ok = lab >= 0
    rows = np.where(ok.mean(1) > 0.5)[0]
    cols = np.where(ok.mean(0) > 0.5)[0]
    return x0 + cols[0], y0 + rows[0], x0 + cols[-1] + 1, y0 + rows[-1] + 1


def edge_frac(px, upper, lower):
    """How much of an anti-aliased pixel is covered by the lower colour (0..1)."""
    v = lower - upper
    return float(np.clip(np.dot(px - upper, v) / np.dot(v, v), 0, 1))


def hill_edges(a, lab, p, upper_ids, hill_id, upper_role, hill_role):
    """For every column: y of the top edge of the hill (sub-pixel), or None if hidden."""
    out = []
    for x in range(a.shape[1]):
        col = lab[:, x]
        idx = np.where(col == hill_id)[0]
        if len(idx) == 0:
            out.append(None)
            continue
        # first hill pixel that has at least 2 more hill pixels in the next 3 (skips noise)
        idx = [i for i in idx if (col[i:i + 3] == hill_id).sum() >= 2]
        if not idx:
            out.append(None)
            continue
        i = idx[0]
        # up to 4 anti-aliased pixels between the upper colour and the hill (steep slopes)
        k = 0
        while k < 4 and i - k - 1 >= 0 and col[i - k - 1] == -1:
            k += 1
        j = i - k  # first row of the transition
        # the edge must sit under 3 rows of the upper colour (not under text or a button)
        if j < 3 or not np.isin(col[j - 3:j], upper_ids).all():
            out.append(None)
            continue
        upper = p[upper_role] if col[j - 1] == ROLES.index(upper_role) else p["sun"]
        # area-preserving edge: each anti-aliased pixel adds the part covered by the hill
        cover = sum(edge_frac(a[r, x].astype(float), upper, p[hill_role]) for r in range(j, i))
        out.append(i - cover)
    return out


def sun_points(a, lab, p):
    """Sub-pixel points on the sun outline where it meets the sky (scanned in rows and columns)."""
    pts = []
    H, W = lab.shape
    for axis in (0, 1):
        L = lab if axis == 0 else lab.T
        A = (a if axis == 0 else a.transpose(1, 0, 2)).astype(float)
        for r in range(L.shape[0]):
            row = L[r]
            n = len(row)
            for i in np.where(row == 1)[0]:
                # entering the sun: 3 sky pixels, up to 4 anti-aliased pixels, then sun
                if i > 0 and row[i - 1] != 1:
                    j = i
                    while j > 0 and i - j < 4 and row[j - 1] == -1:
                        j -= 1
                    if j >= 3 and (row[j - 3:j] == 0).all():
                        cover = sum(edge_frac(A[r, k], p["bg"], p["sun"]) for k in range(j, i))
                        e = i - cover
                        pts.append((e, r + 0.5) if axis == 0 else (r + 0.5, e))
                # leaving the sun: sun, up to 4 anti-aliased pixels, then 3 sky pixels
                if i < n - 1 and row[i + 1] != 1:
                    j = i + 1
                    while j < n and j - i - 1 < 4 and row[j] == -1:
                        j += 1
                    if j + 3 <= n and (row[j:j + 3] == 0).all():
                        cover = sum(edge_frac(A[r, k], p["bg"], p["sun"]) for k in range(i + 1, j))
                        e = i + 1 + cover
                        pts.append((e, r + 0.5) if axis == 0 else (r + 0.5, e))
    pts = np.array(pts)
    if len(pts):
        m = (pts[:, 0] > 2) & (pts[:, 0] < W - 2) & (pts[:, 1] > 2) & (pts[:, 1] < H - 2)
        pts = pts[m]
    return pts


def measure(pal):
    frames = []
    for fam, s, box, scrim in FRAMES:
        p = pal[fam]
        img = np.asarray(Image.open(S % s).convert("RGB"))
        x0, y0, x1, y1 = box
        if scrim is None:
            pad = 6
            x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
            x0, y0, x1, y1 = exact_frame(label(img[y0:y1, x0:x1], p), x0, y0)
        a = img[y0:y1, x0:x1]
        lab = label(a, p)
        if scrim is not None:
            lab[scrim - y0:] = -1  # darkened by the scrim: not the real colours
        frames.append({
            "fam": fam, "screen": s, "box": (int(x0), int(y0), int(x1), int(y1)), "scrim": scrim,
            "back": hill_edges(a, lab, p, (0, 1), 2, "bg", "back"),
            "front": hill_edges(a, lab, p, (2,), 3, "back", "front"),
            "sun": sun_points(a, lab, p),
        })
    return frames


# ---------- 3. master coordinates ----------

def to_master(f, A):
    """Pixel -> master coordinates (master is A units wide and 1 unit high), centre crop."""
    x0, y0, x1, y1 = f["box"]
    W, H = x1 - x0, y1 - y0
    s = max(W / A, H / 1.0)                     # pixels per master unit
    ox, oy = (A - W / s) / 2, (1 - H / s) / 2
    return lambda x, y: (ox + np.asarray(x) / s, oy + np.asarray(y) / s)


def pooled(frames, A, key):
    xs, ys, ids = [], [], []
    for k, f in enumerate(frames):
        m = to_master(f, A)
        for x, y in enumerate(f[key]):
            if y is not None:
                X, Y = m(x + 0.5, y)
                xs.append(X), ys.append(Y), ids.append(k)
    return np.array(xs), np.array(ys), np.array(ids)


def spread(xs, ys, A, n=200):
    """Mean within-bin median absolute deviation: small when all frames trace the same curve
    (median, so a few columns hidden behind text or buttons do not matter)."""
    bins = np.linspace(0, A, n + 1)
    sd = []
    for i in range(n):
        m = (xs >= bins[i]) & (xs < bins[i + 1])
        if m.sum() > 5:
            sd.append(np.median(np.abs(ys[m] - np.median(ys[m]))))
    return float(np.mean(sd))


def fit_circle(pts, w=None):
    """Least-squares circle; w = weight per point (points from bigger frames are more precise)."""
    x, y = pts[:, 0], pts[:, 1]
    w = np.ones(len(x)) if w is None else w
    for _ in range(4):  # refit without outliers (selection rings, text on top of the sun)
        M = np.c_[2 * x, 2 * y, np.ones(len(x))] * w[:, None]
        c, *_ = np.linalg.lstsq(M, (x * x + y * y) * w, rcond=None)
        r = np.sqrt(c[2] + c[0] ** 2 + c[1] ** 2)
        res = np.abs(np.hypot(x - c[0], y - c[1]) - r)
        keep = res < max(3 * np.median(res), 1e-4)
        x, y, w = x[keep], y[keep], w[keep]
    return c[0], c[1], r, float(np.median(res))


def main():
    pal = sample_colours()
    print("Colours (sampled from one clean frame per family; exact-match share in every frame):")
    for fam, p in pal.items():
        print(f"  {fam:6s} " + "  ".join(f"{r} {hexs(p[r])}" for r in ROLES))

    frames = measure(pal)
    for f in frames:
        x0, y0, x1, y1 = f["box"]
        a = np.asarray(Image.open(S % f["screen"]).convert("RGB"))[y0:y1, x0:x1].reshape(-1, 3)
        share = sum((a == pal[f["fam"]][r]).all(1).mean() for r in ROLES)
        f["share"] = share
        print(f"  frame {f['fam']:6s} s{f['screen']:02d} box {f['box']} {x1 - x0}x{y1 - y0} "
              f"(aspect {(x1 - x0) / (y1 - y0):.3f})  palette covers {100 * share:.1f}% of pixels")

    # 3. choose the master aspect ratio where all frames agree
    best = None
    for A in np.arange(0.60, 1.60, 0.01):
        e = sum(spread(*pooled(frames, A, k)[:2], A) for k in ("back", "front"))
        if best is None or e < best[0]:
            best = (e, A)
    for A in np.arange(best[1] - 0.01, best[1] + 0.01, 0.001):
        e = sum(spread(*pooled(frames, A, k)[:2], A) for k in ("back", "front"))
        if e < best[0]:
            best = (e, A)
    print(f"\nBest master aspect ratio (width / height) = {best[1]:.3f}   "
          f"(curve spread {best[0] * 1000:.2f} / 1000 of height)")
    # The best value is a hair under 1: the designer used a square picture. The drawable is
    # square too, so measure everything at exactly 1:1.
    A = 1.0
    e = sum(spread(*pooled(frames, A, k)[:2], A) for k in ("back", "front"))
    print(f"Using a square master (1.000): curve spread {e * 1000:.2f} / 1000 of height")

    # sun: pool the outline points of every frame in master units
    # weight = frame pixels per master unit, so a 1335 px story counts more than a 172 px tile
    use = [f for f in frames if len(f["sun"])]
    pts = np.concatenate([np.c_[to_master(f, A)(f["sun"][:, 0], f["sun"][:, 1])] for f in use])
    w = np.concatenate([np.full(len(f["sun"]), max((f["box"][2] - f["box"][0]) / A,
                                                   f["box"][3] - f["box"][1])) for f in use])
    cx, cy, r, res = fit_circle(pts, w)
    print("  sun outline points per frame:", " ".join(f"{f['fam']}{f['screen']}:{len(f['sun'])}" for f in frames))
    print(f"Sun: centre ({cx / A:.4f} W, {cy:.4f} H), radius {r:.4f} H   (median residual {res * 1000:.2f}/1000)")

    # master curves: median per bin
    curves = {}
    for k in ("back", "front"):
        xs, ys, ids = pooled(frames, A, k)
        bins = np.linspace(0, A, 121)
        c = []
        for i in range(120):
            m = (xs >= bins[i]) & (xs < bins[i + 1])
            if m.sum() > 3:
                c.append(((bins[i] + bins[i + 1]) / 2 / A, float(np.median(ys[m]))))
        curves[k] = c
        # how far each frame is from the consensus curve (in design pixels of that frame)
        cx_, cy_ = np.array(c).T
        for j, f in enumerate(frames):
            m = ids == j
            if m.sum():
                d = np.abs(ys[m] - np.interp(xs[m] / A, cx_, cy_))
                h = max((f["box"][2] - f["box"][0]) / A, f["box"][3] - f["box"][1])
                f.setdefault("err", {})[k] = float(np.median(d) * h)
        print(f"{k:5s} hill top (x as fraction of width, y as fraction of height):")
        print("   " + "  ".join(f"{x:.2f}:{y:.3f}" for x, y in c[::8]))

    print("Median distance of each frame from the consensus (design px): back / front")
    for f in frames:
        e = f.get("err", {})
        print(f"  {f['fam']:6s} s{f['screen']:02d} {str(f['box']):24s} "
              f"{e.get('back', float('nan')):5.2f} / {e.get('front', float('nan')):5.2f}")

    json.dump({"aspect": A, "sun": [cx / A, cy, r],
               "colours": {f: {r: hexs(p[r]) for r in ROLES} for f, p in pal.items()},
               "curves": curves,
               "frames": [{"fam": f["fam"], "screen": f["screen"], "box": f["box"], "scrim": f["scrim"]}
                          for f in frames]},
              open(OUT, "w"), indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
