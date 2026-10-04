"""Compare hand-drawn VectorDrawables with the design PNGs.

For every entry in CHECKS this script
  1. converts res/drawable/<name>.xml to SVG and renders it with PyMuPDF,
  2. crops the matching element from the design PNG (auto-aligned: only position and
     scale are searched, so shape differences still show up),
  3. saves design/check/<label>.png with three panels:
       design crop (zoomed) | my drawing (same zoom) | my drawing at the design's pixel size
     and prints a difference score (mean RGB difference 0..255, lower is better).

Run from the project root:  python tools/check_glyphs.py   (needs: pip install pillow pymupdf numpy)
"""
import os
import xml.etree.ElementTree as ET

import numpy as np
import pymupdf
from PIL import Image, ImageDraw

DRAWABLES = "app/src/main/res/drawable"
SCREENS = "design/screens"
OUT = "design/check"
A = "{http://schemas.android.com/apk/res/android}"
PANEL = 320          # size of each panel in the output image
PX_PER_DP = 707 / 360  # phone frame in the PNGs is 707 px wide = 360 dp

# label, drawable, design image, centre x, centre y, viewport size in design px, tint
# tint: None = drawable's own colours, "auto" = colour of the glyph in the crop
CHECKS = [
    ("logo_png", "logo_kinnect", "design/logo.png", 194.98, 132.25, 232.7, None),
    ("logo_s01_splash", "logo_kinnect", SCREENS + "/screen-01.png", 415.97, 789.8, 117.2, None),
    ("logo_s02_tile", "logo_kinnect", SCREENS + "/screen-02.png", 415.9, 320.9, 72.6, None),
    ("logo_s02_footer", "logo_kinnect", SCREENS + "/screen-02.png", 310, 1548, 24, "auto"),
    ("reaction_like_s05", "reaction_like", SCREENS + "/screen-05.png", 147, 975.5, 63.5, None),
    ("reaction_love_s05", "reaction_love", SCREENS + "/screen-05.png", 244, 944, 89, None),
    ("reaction_haha_s05", "reaction_haha", SCREENS + "/screen-05.png", 341.5, 975.5, 65, None),
    ("reaction_wow_s05", "reaction_wow", SCREENS + "/screen-05.png", 428.5, 975.5, 65, None),
    ("reaction_sad_s05", "reaction_sad", SCREENS + "/screen-05.png", 515.5, 975.5, 65, None),
    ("reaction_angry_s05", "reaction_angry", SCREENS + "/screen-05.png", 602.5, 975.5, 65, None),
    ("reaction_like_s11", "reaction_like", SCREENS + "/screen-11.png", 519, 1527, 61, None),
    ("reaction_love_s11", "reaction_love", SCREENS + "/screen-11.png", 613, 1527, 62, None),
    ("reaction_haha_s11", "reaction_haha", SCREENS + "/screen-11.png", 707, 1527, 62, None),
    ("reaction_haha_small_s04", "reaction_haha", SCREENS + "/screen-04.png", 164.4, 1495.5, 25, None),
    ("reaction_love_s12_float", "reaction_love", SCREENS + "/screen-12.png", 170, 1371, 52, None),
    ("reaction_love_s21_bubble", "reaction_love", SCREENS + "/screen-21.png", 316.5, 910.5, 25, None),
    ("reaction_love_s22_name", "reaction_love", SCREENS + "/screen-22.png", 501, 891, 35, None),
    ("reaction_love_s18_badge", "reaction_love", SCREENS + "/screen-18.png", 181, 460, 35, None),
    ("reaction_like_s18_badge", "reaction_like", SCREENS + "/screen-18.png", 181, 1335, 34, None),
    ("badge_friend_request_s18", "badge_friend_request", SCREENS + "/screen-18.png", 182, 603, 41, None),
    ("badge_comment_s18", "badge_comment", SCREENS + "/screen-18.png", 181.5, 898, 41, None),
    ("badge_group_s18", "badge_group", SCREENS + "/screen-18.png", 182, 1045, 41, None),
    ("badge_tag_s18", "badge_tag", SCREENS + "/screen-18.png", 182, 1190, 41, None),
    ("ic_messenger_s04", "ic_messenger", SCREENS + "/screen-04.png", 703.4, 140, 37.7, "auto"),
    ("ic_messenger_s20_nav", "ic_messenger", SCREENS + "/screen-20.png", 181, 1545, 38, "auto"),
    ("ic_comment_s04", "ic_comment", SCREENS + "/screen-04.png", 352, 1572, 38, "auto"),
    ("ic_create_reel_s20", "ic_create_reel", SCREENS + "/screen-20.png", 650.7, 1544.6, 46, "auto"),
    ("ic_create_reel_s12", "ic_create_reel", SCREENS + "/screen-12.png", 296, 1521, 46, "auto"),
]


# ---------- VectorDrawable -> SVG ----------

def colour(argb):
    """'#AARRGGBB' or '#RRGGBB' -> ('#RRGGBB', opacity)."""
    h = argb.lstrip("#")
    if len(h) == 8:
        return "#" + h[2:], int(h[:2], 16) / 255
    return "#" + h, 1.0


def node_to_svg(node):
    out = []
    for child in node:
        tag = child.tag
        if tag == "group":
            g = lambda k, d: float(child.get(A + k, d))
            px, py = g("pivotX", 0), g("pivotY", 0)
            t = (f"translate({g('translateX', 0)},{g('translateY', 0)}) "
                 f"translate({px},{py}) rotate({g('rotation', 0)}) "
                 f"scale({g('scaleX', 1)},{g('scaleY', 1)}) translate({-px},{-py})")
            out.append(f'<g transform="{t}">' + node_to_svg(child) + "</g>")
        elif tag == "path":
            d = " ".join(child.get(A + "pathData").split())
            attrs = []
            fill = child.get(A + "fillColor")
            if fill:
                c, o = colour(fill)
                attrs.append(f'fill="{c}" fill-opacity="{o * float(child.get(A + "fillAlpha", 1))}"')
            else:
                attrs.append('fill="none"')
            if child.get(A + "fillType") == "evenOdd":
                attrs.append('fill-rule="evenodd"')
            stroke = child.get(A + "strokeColor")
            if stroke:
                c, o = colour(stroke)
                attrs.append(f'stroke="{c}" stroke-opacity="{o}" '
                             f'stroke-width="{child.get(A + "strokeWidth", "0")}" '
                             f'stroke-linecap="{child.get(A + "strokeLineCap", "butt")}" '
                             f'stroke-linejoin="{child.get(A + "strokeLineJoin", "miter")}"')
            out.append(f'<path d="{d}" {" ".join(attrs)}/>')
    return "".join(out)


def render_drawable(name, size):
    """Render res/drawable/<name>.xml to an RGBA PIL image of size x size."""
    root = ET.parse(os.path.join(DRAWABLES, name + ".xml")).getroot()
    vw, vh = root.get(A + "viewportWidth"), root.get(A + "viewportHeight")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
           f'viewBox="0 0 {vw} {vh}">' + node_to_svg(root) + "</svg>")
    doc = pymupdf.open(stream=svg.encode(), filetype="svg")
    pix = doc[0].get_pixmap(alpha=True)
    return Image.frombytes("RGBA", (pix.width, pix.height), pix.samples).resize((size, size))


# ---------- comparison helpers ----------

def crop(img, cx, cy, s, out):
    return img.transform((out, out), Image.EXTENT,
                         (cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2), Image.BICUBIC)


def background_and_ink(c):
    """Background = median of the crop border; ink = pixel colour furthest from it."""
    a = np.asarray(c).reshape(-1, 3).astype(int)
    border = np.concatenate([np.asarray(c)[0], np.asarray(c)[-1],
                             np.asarray(c)[:, 0], np.asarray(c)[:, -1]])
    bg = np.median(border, axis=0).astype(int)
    far = np.abs(a - bg).sum(axis=1)
    ink = np.median(a[far >= np.percentile(far, 97)], axis=0).astype(int)
    return tuple(bg), tuple(ink)


def compose(mine, bg, tint):
    """Put the RGBA drawing on a solid background (optionally recoloured with tint)."""
    if tint is not None:
        solid = Image.new("RGBA", mine.size, tint + (255,))
        solid.putalpha(mine.getchannel("A"))
        mine = solid
    base = Image.new("RGBA", mine.size, bg + (255,))
    return Image.alpha_composite(base, mine).convert("RGB")


def ink_mask(img, bg, dark):
    """Pixels that belong to the glyph's line work: the white parts (faces, hearts, rings),
    or, for a dark icon on a light background, the dark parts."""
    lum = np.asarray(img).astype(int).mean(axis=2)
    if dark:
        return lum < sum(bg) / 3 - 60
    return lum > 200


def score(design_img, cx, cy, s, hi, bg, tint, n=64):
    d = np.asarray(crop(design_img, cx, cy, s, n)).astype(int)
    m = np.asarray(compose(hi.resize((n, n), Image.LANCZOS), bg, tint)).astype(int)
    return np.abs(d - m).mean()


def align(design_img, cx, cy, s, hi, bg, tint):
    """Hill-climb position and scale of the crop to best fit the drawing."""
    p = np.array([cx, cy, s], float)
    step = np.array([s * 0.04, s * 0.04, s * 0.04])
    best = score(design_img, *p, hi, bg, tint)
    while step.max() > s * 0.002:
        moved = False
        for i in range(3):
            for sign in (1, -1):
                q = p.copy()
                q[i] += sign * step[i]
                e = score(design_img, *q, hi, bg, tint)
                if e < best:
                    best, p, moved = e, q, True
        if not moved:
            step /= 2
    return p, best


def main():
    os.makedirs(OUT, exist_ok=True)
    for label, name, src, cx, cy, s, tint in CHECKS:
        design_img = Image.open(src).convert("RGB")
        hi = render_drawable(name, PANEL)
        bg, ink = background_and_ink(crop(design_img, cx, cy, s, 64))
        t = ink if tint == "auto" else None
        (cx, cy, s), err = align(design_img, cx, cy, s, hi, bg, t)

        p1 = crop(design_img, cx, cy, s, PANEL)
        p2 = compose(hi, bg, t)
        native = max(8, round(s))
        p3 = compose(render_drawable(name, native), bg, t).resize((PANEL, PANEL), Image.BICUBIC)

        # Overlay: grey where both agree, red where only the design has ink, blue where only mine has
        dark = t is not None and sum(t) < sum(bg)
        d_ink = ink_mask(p1, bg, dark)
        m_ink = ink_mask(p2, bg, dark)
        ov = np.full(d_ink.shape + (3,), 235, np.uint8)
        ov[d_ink & m_ink] = (150, 150, 150)
        ov[d_ink & ~m_ink] = (220, 40, 40)
        ov[~d_ink & m_ink] = (40, 90, 230)
        p4 = Image.fromarray(ov)

        sheet = Image.new("RGB", (PANEL * 4 + 50, PANEL + 34), "white")
        for i, p in enumerate((p1, p2, p3, p4)):
            sheet.paste(p, (10 + i * (PANEL + 10), 30))
        ImageDraw.Draw(sheet).text(
            (10, 8), f"{label}: design | {name}.xml | at design size ({s:.1f}px = "
                     f"{s / PX_PER_DP:.1f}dp box) | overlay: red = design only, blue = mine only"
                     f"   diff {err:.1f}", fill="black")
        sheet.convert("P", palette=Image.ADAPTIVE, colors=64).save(os.path.join(OUT, label + ".png"),
                                                                    optimize=True)
        print(f"{label:28s} diff {err:5.1f}  centre ({cx:.1f},{cy:.1f}) box {s:.1f}px "
              f"= {s / PX_PER_DP:.1f}dp")


if __name__ == "__main__":
    main()
