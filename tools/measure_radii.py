"""Measure corner radii (dp) of rounded shapes in the design PNGs.

For each shape the script finds its bounding box (pixels close to one colour), then walks down
from the top edge and records how far the left edge is indented on each row. A corner of
radius r is indented r - sqrt(r^2 - (r - d)^2) at depth d, so r is fitted to that profile
(least squares over the rows above the point where the indent reaches zero).

Run from the project root:  python tools/measure_radii.py
"""
import numpy as np

import px

TEAL, CHIP, WHITE, TINT = "#0B5F63", "#ECE9E2", "#FFFFFF", "#E3EFEF"

# label, screen, search box (dp), colour, tolerance
SHAPES = [
    ("input 02 email (white)", 2, (16.8, 300, 342.7, 365), WHITE, 5),
    ("card 02 recent login", 2, (16.8, 205, 342.7, 295), WHITE, 5),
    ("logo tile 02", 2, (141.5, 82, 218, 158), TEAL, 30),
    ("button 02 Log in", 2, (14, 433, 345, 487), TEAL, 30),
    ("input 03 first name", 3, (16.8, 140, 177, 205), WHITE, 6),
    ("input 03 gender female", 3, (16.8, 320, 122, 375), WHITE, 6),
    ("story card 04 OF (night)", 4, (116, 173.6, 217, 340.6), "#2E3A4A", 12),
    ("composer 04 pill border", 4, (60, 106.4, 302, 148), "#D1D1CF", 18),
    ("tray 05 reactions", 5, (11, 423, 307, 479), WHITE, 6),
    ("tooltip 05 Love", 5, (69, 380, 117, 407), "#1C1B19", 25),
    ("bubble 06 comment", 6, (53.5, 102.3, 347.8, 174.6), CHIP, 6),
    ("photo 06 comment (sky)", 6, (56, 520, 200, 640), "#CBD8E9", 8),
    ("chip 07 Public", 7, (69, 89.6, 155.3, 120), TINT, 6),
    ("swatch 07 teal", 7, (51.4, 232.7, 88, 268.8), TEAL, 30),
    ("button 08 SELECT MULTIPLE", 8, (190, 306, 350.3, 346.7), TEAL, 30),
    ("camera 09 preview (sage)", 9, (0, 0, 360, 200), "#CDDAC0", 8),
    ("gallery 09 thumb (teal sky)", 9, (10, 590, 60, 640), "#BFD7D9", 10),
    ("pill 10 Your story", 10, (9, 708.3, 153, 758.2), "#2A2925", 8),
    ("tag 10 Saturday plans", 10, (25, 395, 210, 445), "#B84A2A", 25),
    ("button 13 Join", 13, (286.7, 419, 349.3, 457.7), TEAL, 30),
    ("avatar 13 OP", 13, (11, 411, 66, 465), "#7A4E7F", 30),
    ("button 13 See all people", 13, (11.7, 325.4, 349.3, 367.1), CHIP, 6),
    ("chip 14 Suggestions", 14, (21.9, 109.5, 127.3, 149.2), CHIP, 6),
    ("button 14 Confirm", 14, (106.9, 241.9, 230.6, 282.6), TEAL, 30),
    ("button 15 Add to story", 15, (11.7, 386.5, 155.3, 429.7), TEAL, 30),
    ("chip 15 Posts tab", 15, (11.7, 435.8, 76.4, 475), TINT, 5),
    ("tile 15 friend LM", 15, (11, 698, 121, 777), "#7A4E7F", 30),
    ("cover 16 (teal sky)", 16, (13.2, 242.4, 347.8, 357), "#BFD7D9", 6),
    ("photo 17 grid night", 17, (13.2, 619.2, 125.3, 728.6), "#2E3A4A", 12),
    ("button 18 Confirm", 18, (77.9, 275.4, 192.5, 316), TEAL, 30),
    ("button 18 See previous", 18, (11.7, 657.3, 349.3, 700.6), CHIP, 6),
    ("card 19 profile", 19, (11.7, 100, 349.3, 176), WHITE, 4),
    ("card 19 memories", 19, (11.7, 200, 179.7, 290), WHITE, 4),
    ("button 19 See more", 19, (11.7, 448.6, 349.3, 493.4), CHIP, 6),
    ("button 19 Log out", 19, (11.7, 649.7, 349.3, 699), CHIP, 6),
    ("input 20 search", 20, (11.7, 52.4, 349.3, 96.2), CHIP, 6),
    ("bubble 21 received (first)", 21, (42.2, 233.7, 294.3, 271.4), CHIP, 6),
    ("bubble 21 sent (first)", 21, (233, 347.8, 351.3, 387.5), TEAL, 30),
    ("photo 21 chat (lilac)", 21, (161.9, 517.3, 351.3, 651.2), "#D8C7D9", 8),
    ("avatar 22 AM", 22, (103, 209, 256, 362), "#7A4E7F", 30),
    ("button 22 end call", 22, (174.7, 648.2, 256, 728.6), "#C62827", 25),
    ("label 23 JUST LISTED", 23, (19.3, 199, 103.3, 222), "#B84A2A", 25),
    ("tile 23 product (sage)", 23, (13.2, 191.5, 178.2, 357), "#CDDAC0", 8),
    ("chip 23 Sell", 23, (13.2, 105.4, 178.2, 145), CHIP, 6),
]


def fit_radius(indent):
    """Fit r (px) to the indent profile of a corner (indent[d] = left indent at depth d)."""
    best, best_err = 0, 1e9
    for r in np.arange(1, 120, 0.25):
        d = np.arange(len(indent)) + 0.5
        model = np.where(d < r, r - np.sqrt(np.maximum(r * r - (r - d) ** 2, 0)), 0)
        n = int(min(len(indent), r + 2))
        err = np.mean((model[:n] - indent[:n]) ** 2)
        if err < best_err:
            best, best_err = r, err
    return best


if __name__ == "__main__":
    cache = {}
    for label, n, box, colour, tol in SHAPES:
        if n not in cache:
            cache[n] = px.load(n)
        a = cache[n]
        x0, y0 = px.to_px(n, box[0], box[1])
        x1, y1 = px.to_px(n, box[2], box[3])
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        target = np.array([int(colour[i:i + 2], 16) for i in (1, 3, 5)])
        m = np.abs(a[y0:y1, x0:x1] - target).max(axis=2) <= tol
        ys, xs = np.where(m)
        if len(xs) == 0:
            print("%-30s no match" % label)
            continue
        top, left, bottom = ys.min(), xs.min(), ys.max()
        indent = []
        for y in range(top, min(top + 120, bottom)):
            row = np.where(m[y])[0]
            indent.append((row.min() - left) if len(row) else 0)
        indent = np.array(indent, float)
        r = fit_radius(indent)
        h = (bottom - top + 1) / px.PX_PER_DP
        print("%-30s radius %5.1f dp   (height %5.1f dp%s)"
              % (label, r / px.PX_PER_DP, h, ", pill" if r / px.PX_PER_DP > h / 2 - 1.5 else ""))
