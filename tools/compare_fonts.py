"""Compare candidate Google Fonts with text crops from the design PNGs.

For each design sample (a line of text, cropped to its ink) and each candidate font + weight:
  1. render the same text with Pillow, crop it to its ink,
  2. report the width/height ratio against the design (a different face has different widths),
  3. scale the render onto the design crop's box and report the overlap (IoU of the inked pixels).
Higher IoU and a ratio near 1.00 mean a closer face. A sheet per sample is written to
design/check/font_<sample>.png: the design crop on top, then the best candidates.

Usage (run from the project root, fonts = folder of .ttf files from github.com/google/fonts):
  python tools/compare_fonts.py <fonts folder>
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import px

# name, screen, box (dp) around one line of text, text, ink colour, candidate weights
SAMPLES = [
    ("heading_03", 3, (15, 74, 275, 101), "What's your name and", "#1C1B19", (700, 800)),
    ("heading_03b", 3, (15, 100, 160, 128), "birthday?", "#1C1B19", (700, 800)),
    ("wordmark_04", 4, (14, 12, 115, 38), "kinnect", "#0B5F63", (700, 800)),
    ("title_18", 18, (14, 12, 160, 38), "Notifications", "#1C1B19", (700, 800)),
    ("name_15", 15, (14, 305, 160, 330), "Jacob West", "#1C1B19", (700, 800)),
    ("body_04", 4, (14, 410, 346, 433), "Sunset walk with the crew. Worth every grain of sand",
     "#1C1B19", (400, 500)),
    ("body_04b", 4, (72, 117, 262, 139), "What's on your mind, Jacob?", "#5B5954", (400, 500)),
    ("body_02", 2, (90, 252, 165, 272), "Tap to log in", "#5B5954", (400, 500)),
    ("body_19", 19, (192, 250, 240, 272), "Saved", "#1C1B19", (400, 500)),
    ("bold_04", 4, (60, 368, 133, 388), "Lina Marsh", "#1C1B19", (600, 700)),
    ("button_02", 2, (140, 450, 220, 470), "Log in", "#FFFFFF", (600, 700)),
]

HEADING_FONTS = ["BricolageGrotesque", "FamiljenGrotesk", "SchibstedGrotesk", "Gabarito",
                 "InstrumentSans", "HankenGrotesk", "Onest", "Parkinsans", "FunnelDisplay",
                 "HostGrotesk", "RethinkSans", "Archivo", "Sora"]
BODY_FONTS = ["Figtree", "AlbertSans", "PlusJakartaSans", "DMSans", "Outfit", "Urbanist",
              "Onest", "GolosText", "Manrope", "RethinkSans"]


def ink_mask(img_rgb, colour):
    """Boolean mask of inked pixels: closer in brightness to the ink than to the background.

    A midpoint threshold keeps thin anti-aliased strokes (body text) that a strict colour
    match would drop."""
    gray = img_rgb.astype(float).mean(axis=2)
    ink = np.mean([int(colour[i:i + 2], 16) for i in (1, 3, 5)])
    bg = np.median(gray)
    mid = (ink + bg) / 2
    return gray < mid if ink < bg else gray > mid


def crop_to_ink(mask):
    ys, xs = np.where(mask)
    return mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def render(path, weight, text, size):
    font = ImageFont.truetype(path, size)
    try:
        axes = font.get_variation_axes()
        values = []
        for ax in axes:
            name = ax["name"] if isinstance(ax["name"], str) else ax["name"].decode()
            if name.lower().startswith("weight"):
                values.append(weight)
            elif name.lower().startswith("optical"):
                values.append(max(ax["minimum"], min(ax["maximum"], 24)))
            else:
                values.append(ax["default"])
        font.set_variation_by_axes(values)
    except OSError:
        pass  # static font
    w = int(size * len(text) * 0.9) + 40
    img = Image.new("L", (w, size * 2), 0)
    ImageDraw.Draw(img).text((20, size // 3), text, font=font, fill=255)
    return np.asarray(img) > 128


def main():
    font_dir = sys.argv[1]
    files = {f.split("[")[0].split(".")[0]: os.path.join(font_dir, f)
             for f in os.listdir(font_dir) if f.endswith(".ttf")}
    for name, n, box, text, colour, weights in SAMPLES:
        a = px.load(n)
        x0, y0 = px.to_px(n, box[0], box[1])
        x1, y1 = px.to_px(n, box[2], box[3])
        crop = a[int(y0):int(y1), int(x0):int(x1)].astype(np.uint8)
        design = crop_to_ink(ink_mask(crop, colour))
        dh, dw = design.shape
        fonts = BODY_FONTS if name.startswith(("body", "bold", "button")) else HEADING_FONTS
        results = []
        for fam in fonts:
            if fam not in files:
                continue
            for wt in weights:
                r = crop_to_ink(render(files[fam], wt, text, 80))
                ratio = (r.shape[1] / r.shape[0]) / (dw / dh)
                scaled = np.asarray(Image.fromarray(r.astype(np.uint8) * 255).resize(
                    (dw, dh), Image.BILINEAR)) > 128
                iou = (scaled & design).sum() / float((scaled | design).sum())
                results.append((iou, ratio, fam, wt, scaled))
        results.sort(key=lambda t: -t[0])
        print("== %s  \"%s\"  (design ink %d x %d px)" % (name, text, dw, dh))
        for iou, ratio, fam, wt, _ in results[:8]:
            print("   IoU %.3f   width ratio %.3f   %s %d" % (iou, ratio, fam, wt))
        # Sheet: design, then the top 5 (scaled onto the design box), labelled.
        rows = [("design", design)] + [("%s %d" % (f, w), s) for _, _, f, w, s in results[:5]]
        sheet = Image.new("RGB", (dw + 220, (dh + 10) * len(rows) + 10), "white")
        d = ImageDraw.Draw(sheet)
        for i, (label, m) in enumerate(rows):
            y = 10 + i * (dh + 10)
            sheet.paste(Image.fromarray(255 - m.astype(np.uint8) * 255).convert("RGB"), (210, y))
            d.text((5, y + dh // 2 - 6), label, fill="black")
        sheet.save("design/check/font_%s.png" % name)


if __name__ == "__main__":
    main()
