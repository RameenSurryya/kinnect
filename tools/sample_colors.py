"""Sample the exact design colours from the PNGs (for res/values/colors.xml).

The PNGs carry slight compression noise (a flat teal reads #0B5F63 +/- 3), so a colour is never
read from one pixel. Two robust methods:

  mode : the dominant flat colour of a box. Pixels are grouped into 8-level buckets per channel;
         the fullest bucket wins and the result is the median of its pixels. Use it for fills
         (buttons, avatars, chips, backgrounds) even when a few letters sit on top.
  ink  : the colour of thin text or icon strokes in a box. Takes the pixels that differ most
         from the dominant (background) colour (the top 15 % of the distance range) and returns
         their median, so anti-aliased edges do not lighten the result.

Boxes are in dp from the screen's top-left corner (tools/px.py explains the scale).
Run from the project root:  python tools/sample_colors.py
"""
import numpy as np
from PIL import Image

import px  # tools/px.py: PNG loading and dp -> px conversion

# name, screen, (x0, y0, x1, y1) in dp, method
SAMPLES = [
    # Brand and surfaces
    ("teal (Log in button)", 2, (25, 445, 60, 475), "mode"),
    ("teal (04 tab underline)", 4, (5, 93.6, 65, 95.6), "mode"),
    ("teal (14 Confirm)", 14, (110, 249, 130, 268), "mode"),
    ("off-white bg (02)", 2, (20, 560, 340, 640), "mode"),
    ("off-white bg (19)", 19, (20, 720, 340, 770), "mode"),
    ("off-white bg (03)", 3, (20, 700, 340, 770), "mode"),
    ("white bg (04)", 4, (20, 115, 60, 125), "mode"),
    ("white card (19 profile card)", 19, (200, 120, 300, 130), "mode"),
    ("white input (02)", 2, (200, 330, 300, 350), "mode"),
    ("chip fill (04 search circle)", 4, (266, 30, 272, 40), "mode"),
    ("chip fill (19 See more)", 19, (20, 460, 100, 480), "mode"),
    ("chip fill (14 Delete)", 14, (225, 249, 240, 268), "mode"),
    ("chip fill (13 Posts chip)", 13, (138, 62, 145, 85), "mode"),
    ("chip fill (13 search box)", 13, (120, 15, 180, 20), "mode"),
    ("bubble (06 comment)", 6, (250, 110, 330, 120), "mode"),
    ("bubble received (21)", 21, (260, 240, 285, 265), "mode"),
    ("divider (04 under tabs)", 4, (100, 96.2, 360, 97.3), "mode"),
    ("divider (19 rows)", 19, (60, 499.5, 300, 501), "mode"),
    ("divider (14 section)", 14, (60, 597, 300, 598.5), "mode"),
    ("divider (04 like row)", 4, (40, 734.5, 300, 735.6), "mode"),
    ("input border (02)", 2, (100, 309.2, 250, 310.4), "mode"),
    ("frame outline", 2, (100, -0.8, 250, -0.2), "mode"),
    ("section band (04)", 4, (20, 158.5, 340, 164.5), "mode"),
    ("section band (04 second)", 4, (20, 349, 340, 354), "mode"),
    ("progress track (03)", 3, (240, 48.8, 335, 51.5), "mode"),
    ("strength grey (03)", 3, (205, 508.8, 285, 512.6), "mode"),
    ("strength orange (03)", 3, (22, 508.8, 100, 512.6), "mode"),
    ("highlight band (18 New)", 18, (300, 175, 345, 200), "mode"),
    ("selected chip (13 All)", 13, (17, 62, 24, 85), "mode"),
    ("selected chip (15 Posts)", 15, (17, 393, 24, 412), "mode"),
    ("add-friend circle (13)", 13, (310, 225, 316, 240), "mode"),
    ("public chip fill (07)", 7, (74, 98, 78, 112), "mode"),
    ("public chip border (07)", 7, (71.3, 96, 72.3, 112), "mode"),
    ("bubble sent (21)", 21, (300, 360, 340, 375), "mode"),
    # Accents (07 colour swatches are the cleanest flat samples)
    ("swatch teal (07)", 7, (58, 238, 82, 262), "mode"),
    ("swatch orange-red (07)", 7, (96, 238, 120, 262), "mode"),
    ("swatch indigo (07)", 7, (135, 238, 159, 262), "mode"),
    ("swatch green (07)", 7, (173, 238, 197, 262), "mode"),
    ("swatch mustard (07)", 7, (212, 238, 236, 262), "mode"),
    ("swatch purple (07)", 7, (251, 238, 275, 262), "mode"),
    ("swatch black (07)", 7, (289, 238, 313, 262), "mode"),
    ("badge (04 messenger)", 4, (333, 9, 344, 18), "mode"),
    ("badge (02 avatar)", 2, (68, 231, 80, 241), "mode"),
    ("just listed (23)", 23, (24, 201.5, 66, 218.5), "mode"),
    ("love red (05 reaction)", 5, (75, 415, 112, 452), "mode"),
    ("haha mustard (05 reaction)", 5, (127, 437, 156, 466), "mode"),
    ("angry (05 reaction)", 5, (260, 437, 290, 466), "mode"),
    ("like teal (05 reaction)", 5, (27, 437, 57, 466), "mode"),
    ("online green (20 AK dot)", 20, (57.5, 236, 62.5, 241), "mode"),
    ("unread dot teal (20)", 20, (334, 216, 341, 222), "mode"),
    ("unread dot red (20)", 20, (332, 349, 339, 356), "mode"),
    ("close friends green (10)", 10, (172, 719, 186, 733), "mode"),
    # Dark screens
    ("camera bg (09)", 9, (5, 700, 30, 770), "mode"),
    ("story bg (11)", 11, (5, 700, 30, 770), "mode"),
    ("story bg (12)", 12, (5, 700, 30, 770), "mode"),
    ("story pill (10 Your story)", 10, (130, 722, 145, 745), "mode"),
    ("story input border (11)", 11, (12.5, 720, 13.3, 740), "mode"),
    ("camera btn on sage (09 brightness)", 9, (16, 24, 22, 48), "mode"),
    ("camera btn dark (09 flash)", 9, (80, 650, 86, 665), "mode"),
    ("shutter ring (09)", 9, (140.5, 655, 142.5, 665), "mode"),
    ("story editor btn (10)", 10, (16, 24, 22, 48), "mode"),
    ("story name scrim (04 Omar)", 4, (120, 297, 128, 310), "mode"),
    ("call bg (22)", 22, (20, 300, 340, 400), "mode"),
    ("call control (22)", 22, (40, 670, 50, 705), "mode"),
    ("call end red (22)", 22, (185, 660, 200, 715), "mode"),
    ("call halo outer (22)", 22, (90, 280, 95, 290), "mode"),
    ("call halo inner (22)", 22, (101, 280, 105, 290), "mode"),
    ("photo expand btn (08)", 8, (14, 318, 20, 335), "mode"),
    ("dim overlay over white (05 bg)", 5, (20, 720, 340, 770), "mode"),
    ("dim overlay over tooltip (05 Love)", 5, (72, 383, 76, 393), "mode"),
    # Text (ink = darkest stroke colour)
    ("text dark (04 Lina Marsh)", 4, (61.6, 371, 131, 385), "ink"),
    ("text dark (14 Sara Iqbal)", 14, (110, 196, 180, 212), "ink"),
    ("text dark (02 Jacob West)", 2, (94, 236, 177, 252), "ink"),
    ("text body (04 post text)", 4, (15, 418, 330, 430), "ink"),
    ("text grey (04 2h)", 4, (61.6, 389, 71, 401), "ink"),
    ("text grey (14 mutual friends)", 14, (142.6, 222.5, 229.6, 234.7), "ink"),
    ("text grey (19 See your profile)", 19, (78.4, 143, 168, 156), "ink"),
    ("text grey (23 Clifton)", 23, (15, 399, 50, 409), "ink"),
    ("text grey (13 subtitle)", 13, (74, 172.6, 197, 184.8), "ink"),
    ("text grey (03 Step 2 of 3)", 3, (282.6, 18.3, 341, 31), "ink"),
    ("text grey (02 English UK)", 2, (136.4, 33.6, 206.7, 46.3), "ink"),
    ("text grey (02 RECENT LOGIN)", 2, (19.3, 190.4, 112.5, 202.6), "ink"),
    ("text grey (02 input label)", 2, (33, 320, 150, 331.5), "ink"),
    ("text grey (02 footer)", 2, (160, 737, 241, 749), "ink"),
    ("text grey (19 All shortcuts)", 19, (15, 183.8, 90.6, 195.5), "ink"),
    ("text grey (16 placeholder)", 16, (111, 490.8, 164.5, 504.6), "ink"),
    ("text grey (06 2h)", 6, (66.7, 178.7, 80.4, 190.4), "ink"),
    ("text grey (06 Reply)", 6, (127.8, 178.7, 158.3, 190.4), "ink"),
    ("text grey (21 TODAY)", 21, (136.5, 212.8, 224, 223), "ink"),
    ("text grey (08 Photo tab)", 8, (161, 746.5, 200, 759), "ink"),
    ("text grey (20 Your note)", 20, (20, 163.4, 69, 174.6), "ink"),
    ("text grey (20 preview)", 20, (78, 361, 210, 373), "ink"),
    ("text teal (14 See all)", 14, (313, 169, 354, 181), "ink"),
    ("text teal (02 Forgot)", 2, (123.7, 506, 236.8, 520), "ink"),
    ("text teal (18 5m)", 18, (81.5, 185.3, 99.8, 195.5), "ink"),
    ("text orange (14 count 12)", 14, (172, 166, 191, 180), "ink"),
    ("text white-ish (22 encrypted)", 22, (123.7, 46.8, 254.6, 59.6), "ink"),
    ("text camera mode grey (09 TEXT)", 9, (16, 714, 50, 724), "ink"),
    ("icon grey (04 tab menu)", 4, (314, 65, 334, 81), "ink"),
    ("icon grey (04 friends tab)", 4, (97, 63, 120, 84), "ink"),
    ("icon dark (04 search)", 4, (274, 18, 292, 36), "ink"),
    ("icon grey (04 more dots)", 4, (285, 372, 304, 378), "ink"),
    ("icon grey (13 clock)", 13, (24, 534, 40, 549), "ink"),
    # Shortcut icons (19) and create-post actions (07)
    ("19 memories icon", 19, (28, 219, 49, 240), "ink"),
    ("19 saved icon", 19, (197, 219, 214, 240), "ink"),
    ("19 groups icon", 19, (27, 298, 50, 320), "ink"),
    ("19 marketplace icon", 19, (195, 298, 217, 320), "ink"),
    ("19 friends icon", 19, (28, 377, 50, 399), "ink"),
    ("19 events icon", 19, (195, 377, 217, 399), "ink"),
    ("07 photo icon", 7, (20, 474, 40, 492), "ink"),
    ("07 tag icon", 7, (20, 518, 40, 536), "ink"),
    ("07 feeling icon", 7, (20, 562, 40, 580), "ink"),
    ("07 check-in icon", 7, (22, 606, 38, 624), "ink"),
    ("07 live icon", 7, (20, 650, 40, 668), "ink"),
    ("07 camera icon", 7, (20, 694, 40, 712), "ink"),
    ("07 event icon", 7, (20, 738, 40, 756), "ink"),
    # Initials avatars (the disc wins the mode even with letters on top)
    ("avatar JW (04)", 4, (17, 110.5, 50, 143.5), "mode"),
    ("avatar LM (04)", 4, (17, 370, 50, 403), "mode"),
    ("avatar AK (18)", 18, (17, 145, 68, 196), "mode"),
    ("avatar SI (18)", 18, (17, 218, 68, 270), "mode"),
    ("avatar ZR (18)", 18, (17, 371, 68, 422), "mode"),
    ("avatar DC (18)", 18, (17, 444, 68, 495), "mode"),
    ("avatar HA (18)", 18, (17, 518, 68, 569), "mode"),
    ("avatar LM (18)", 18, (17, 591, 68, 642), "mode"),
    ("avatar OF (17)", 17, (125, 165, 235, 270), "mode"),
    ("avatar MC (06)", 6, (17, 647, 46, 676), "mode"),
    ("avatar BA (20)", 20, (17, 461, 64, 508), "mode"),
    ("avatar NF (20)", 20, (17, 527, 64, 574), "mode"),
    ("avatar SI (14)", 14, (27, 197, 95, 265), "mode"),
    ("avatar BA (14)", 14, (27, 298, 95, 366), "mode"),
    ("avatar NF (14)", 14, (27, 398, 95, 466), "mode"),
    ("avatar DS (14)", 14, (27, 501, 95, 569), "mode"),
    ("avatar OS (13)", 13, (17, 210, 61, 254), "mode"),
    ("avatar OT (13)", 13, (17, 272, 61, 316), "mode"),
    ("avatar OP (13)", 13, (17, 416, 61, 460), "mode"),
    ("avatar AM (22)", 22, (112, 218, 248, 352), "mode"),
    ("avatar AK (21 big)", 21, (148, 75, 212, 135), "mode"),
    ("avatar HA (20 note)", 20, (292, 108, 340, 150), "mode"),
]


def sample(a, n, box, method):
    x0, y0 = px.to_px(n, box[0], box[1])
    x1, y1 = px.to_px(n, box[2], box[3])
    region = a[int(round(y0)):max(int(round(y1)), int(round(y0)) + 1),
               int(round(x0)):max(int(round(x1)), int(round(x0)) + 1)].reshape(-1, 3)
    buckets = region // 32
    keys, inv, counts = np.unique(buckets, axis=0, return_inverse=True, return_counts=True)
    dominant = np.median(region[inv.ravel() == counts.argmax()], axis=0)
    if method == "mode":
        return dominant, 100.0 * counts.max() / len(region)
    dist = np.abs(region - dominant).sum(axis=1)
    core = region[dist >= dist.max() * 0.85]
    return np.median(core, axis=0), 100.0 * len(core) / len(region)


if __name__ == "__main__":
    cache = {}
    for name, n, box, method in SAMPLES:
        if n not in cache:
            cache[n] = px.load(n)
        c, share = sample(cache[n], n, box, method)
        print("%-40s %s   (%s, %4.1f%% of box)" % (name, px.hexc(c), method, share))
