"""Measure text sizes (sp) in the design PNGs.

For each sample the same string is rendered with the chosen font at 100 px, both renders are
cropped to their ink, and the size is solved from the ratio of the ink boxes:
  size_from_height = 100 px * design_ink_height / render_ink_height / 1.964 px-per-dp
  size_from_width  = the same with widths
Height is unaffected by letter spacing; width is more precise on long strings. When the two
agree the text has no extra letter spacing; when the width estimate is larger the text is
tracked out (letterSpacing = width/height - 1, roughly).

Usage (run from the project root):  python tools/measure_text.py <fonts folder>
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import px
from compare_fonts import crop_to_ink, ink_mask

B, F = "BricolageGrotesque", "Figtree"
DARK, GREY, TEAL, WHITE = "#1C1B19", "#5B5954", "#0B5F63", "#FFFFFF"

# label, screen, box (dp), text, ink colour, family, weight
SAMPLES = [
    ("wordmark 04", 4, (14, 12, 115, 38), "kinnect", TEAL, B, 800),
    ("heading 03 (large)", 3, (15, 74, 275, 101), "What's your name and", DARK, B, 700),
    ("page title 18", 18, (14, 12, 160, 38), "Notifications", DARK, B, 700),
    ("page title 14", 14, (11.3, 7.9, 111.3, 33.9), "Friends", DARK, B, 700),
    ("page title 23", 23, (14, 12, 160, 40), "Marketplace", DARK, B, 700),
    ("page title 20 Chats", 20, (40, 12, 120, 40), "Chats", DARK, B, 700),
    ("bar title 03", 3, (45, 12, 182, 35), "Create account", DARK, B, 700),
    ("bar title 06", 6, (45, 15, 145, 37), "Comments", DARK, B, 700),
    ("bar title 15", 15, (45, 15, 145, 37), "Jacob West", DARK, B, 700),
    ("bar title 16 (centred)", 16, (130, 15, 235, 37), "Edit profile", DARK, B, 700),
    ("section 14 Friend requests", 14, (13.3, 157.9, 157.3, 179.9), "Friend requests", DARK, B, 700),
    ("section 18 New", 18, (13, 110, 55, 129), "New", DARK, B, 700),
    ("section 13 People", 13, (13, 114, 75, 133), "People", DARK, B, 700),
    ("section 23 Today's picks", 23, (13, 160, 138, 182), "Today's picks", DARK, B, 700),
    ("section 15 Details", 15, (13, 503, 80, 520), "Details", DARK, B, 700),
    ("profile name 15", 15, (13, 304, 155, 332), "Jacob West", DARK, B, 800),
    ("profile name 17", 17, (100, 298, 260, 325), "Omar Farooq", DARK, B, 800),
    ("chat name 21", 21, (125, 148, 235, 171), "Aisha Khan", DARK, B, 700),
    ("body 04 post", 4, (14, 410, 346, 433), "Sunset walk with the crew. Worth every grain of sand",
     DARK, F, 400),
    ("body 04 composer hint", 4, (72, 117, 262, 139), "What's on your mind, Jacob?", GREY, F, 400),
    ("name 04 Lina Marsh", 4, (60, 368, 133, 388), "Lina Marsh", DARK, F, 600),
    ("name 14 Sara Iqbal", 14, (97.3, 192.9, 173.3, 211.9), "Sara Iqbal", DARK, F, 600),
    ("name 02 Jacob West", 2, (92, 235, 180, 254), "Jacob West", DARK, F, 600),
    ("subtitle 14 mutual", 14, (131.3, 215.9, 223.3, 232.9), "8 mutual friends", GREY, F, 400),
    ("subtitle 02 Tap to log in", 2, (90, 252, 165, 272), "Tap to log in", GREY, F, 400),
    ("subtitle 13 Friend Lives", 13, (72, 171, 200, 186), "Friend · Lives in Karachi", GREY, F, 400),
    ("caption 04 2h", 4, (60, 387, 74, 402), "2h", GREY, F, 400),
    ("caption 23 Clifton", 23, (13, 397, 52, 411), "Clifton", GREY, F, 400),
    ("meta 06 Reply", 6, (125, 177, 161, 192), "Reply", GREY, F, 600),
    ("label 02 RECENT LOGIN", 2, (17, 188, 115, 205), "RECENT LOGIN", GREY, F, 700),
    ("label 19 All shortcuts", 19, (13, 182, 93, 197), "All shortcuts", GREY, F, 600),
    ("input label 02", 2, (31, 318, 152, 333), "Mobile number or email", GREY, F, 400),
    ("input value 02", 2, (31, 335, 180, 352), "jacob.west@mail.com", DARK, F, 400),
    ("button 02 Log in", 2, (140, 450, 220, 470), "Log in", WHITE, F, 700),
    ("button 02 Create new account", 2, (105, 680, 255, 700), "Create new account", TEAL, F, 700),
    ("button 14 Confirm", 14, (116.3, 247.9, 186.3, 265.9), "Confirm", WHITE, F, 700),
    ("button 18 Confirm", 18, (100, 286, 165, 304), "Confirm", WHITE, F, 700),
    ("button 19 See more", 19, (140, 461, 220, 480), "See more", DARK, F, 700),
    ("button 13 Join", 13, (300, 430, 335, 447), "Join", WHITE, F, 700),
    ("chip 14 Suggestions", 14, (26.3, 115.9, 106.3, 134.9), "Suggestions", DARK, F, 700),
    ("chip 13 People", 13, (72, 63, 120, 82), "People", DARK, F, 700),
    ("chip 23 Sell", 23, (95, 117, 120, 135), "Sell", DARK, F, 700),
    ("tab 08 Gallery", 8, (30, 744, 90, 762), "Gallery", TEAL, F, 700),
    ("nav 20 People", 20, (160, 758, 200, 771), "People", GREY, F, 600),
    ("badge 04 3", 4, (334, 8, 343, 18), "3", WHITE, F, 700),
    ("badge 04 5", 4, (259, 61, 270, 71), "5", WHITE, F, 700),
    ("label 23 JUST LISTED", 23, (25, 204, 98, 217), "JUST LISTED", WHITE, F, 700),
    ("shortcut 19 Memories", 19, (25, 253, 90, 268), "Memories", DARK, F, 500),
    ("menu row 19 Help", 19, (60, 512, 170, 534), "Help & support", DARK, F, 500),
    ("see all 14", 14, (301.3, 162.9, 347.3, 178.9), "See all", TEAL, F, 600),
    ("time 14 3d", 14, (331.3, 192.9, 348.3, 205.9), "3d", GREY, F, 400),
    ("chat bubble 21", 21, (55, 243, 280, 262), "Hey! Are you still coming Saturday?", DARK, F, 400),
    ("chat header name 21", 21, (92, 8, 180, 31), "Aisha Khan", DARK, B, 700),
    ("chat header name 21 (Figtree)", 21, (92, 8, 180, 31), "Aisha Khan", DARK, F, 700),
    ("chat status 21", 21, (92, 31, 170, 46), "Active now", GREY, F, 400),
    ("chat intro 21", 21, (60, 175, 300, 192), "You're friends on Kinnect · Lives in Karachi",
     GREY, F, 400),
    ("chat time 21", 21, (125, 210, 235, 225), "TODAY 4:49 PM", GREY, F, 600),
    ("chat replied 21", 21, (240, 440, 350, 454), "You replied to Aisha", GREY, F, 400),
    ("chat sent 21", 21, (138, 393, 345, 413), "Already charged both batteries", WHITE, F, 400),
    ("chat Aa 21", 21, (170, 735, 200, 753), "Aa", "#74726E", F, 400),
    ("call encrypted 22", 22, (120, 45, 260, 62), "End-to-end encrypted", "#CFDFE0", F, 400),
    ("call name 22", 22, (125, 395, 210, 422), "Ammi", WHITE, B, 800),
    ("call timer 22", 22, (150, 434, 210, 453), "03:12", "#CFDFE0", F, 400),
    ("call initials 22", 22, (160, 260, 205, 310), "AM", WHITE, B, 700),
    ("comment name 06", 6, (63, 109, 120, 124), "Aisha Khan", DARK, F, 600),
    ("comment text 06", 6, (63, 125, 310, 141), "That sky is unreal. Which part of the beach",
     DARK, F, 400),
    ("splash from 01", 1, (160, 685, 200, 697), "from", "#CFE7E6", F, 400),
    ("splash SMD 01", 1, (145, 699, 215, 717), "SMD", WHITE, F, 700),
    ("story name 04 Omar", 4, (120, 318, 195, 333), "Omar Farooq", WHITE, F, 600),
    ("step 03", 3, (280, 16, 343, 33), "Step 2 of 3", GREY, F, 400),
]


def render(path, weight, text, size=100):
    font = ImageFont.truetype(path, size)
    axes = font.get_variation_axes()
    vals = []
    for ax in axes:
        nm = ax["name"].decode() if isinstance(ax["name"], bytes) else ax["name"]
        vals.append(weight if nm.lower().startswith("weight")
                    else min(max(24, ax["minimum"]), ax["maximum"]) if nm.lower().startswith("optical")
                    else ax["default"])
    font.set_variation_by_axes(vals)
    img = Image.new("L", (int(size * len(text) * 0.9) + 60, size * 2), 0)
    ImageDraw.Draw(img).text((30, size // 3), text, font=font, fill=255)
    return np.asarray(img) > 128


def main():
    d = sys.argv[1]
    files = {f.split("[")[0]: os.path.join(d, f) for f in os.listdir(d) if f.endswith(".ttf")}
    for label, n, box, text, colour, fam, wt in SAMPLES:
        a = px.load(n)
        x0, y0 = px.to_px(n, box[0], box[1])
        x1, y1 = px.to_px(n, box[2], box[3])
        design = crop_to_ink(ink_mask(a[int(y0):int(y1), int(x0):int(x1)].astype(np.uint8), colour))
        r = crop_to_ink(render(files[fam], wt, text))
        sh = 100.0 * design.shape[0] / r.shape[0] / px.PX_PER_DP
        sw = 100.0 * design.shape[1] / r.shape[1] / px.PX_PER_DP
        print("%-30s height->%5.1f sp  width->%5.1f sp   (%s %d)" % (label, sh, sw, fam, wt))


if __name__ == "__main__":
    main()
