"""Measure element sizes (dp) in the design PNGs, for res/values/dimens.xml.

Each entry finds the bounding box of the pixels close to one colour inside a search box
(tools/px.py bbox), so the printed size is the element's real edge-to-edge size in dp.
Anti-aliasing adds up to ~0.5 dp, so sizes are rounded to the nearest whole dp in dimens.xml.

Run from the project root:  python tools/measure_dims.py
"""
import numpy as np

import px

TEAL, CHIP, WHITE = "#0B5F63", "#ECE9E2", "#FFFFFF"
TINT = "#E3EFEF"  # light teal: selected chip, highlight band, add-friend circle

# label, screen, search box (x0, y0, x1, y1) in dp, colour, tolerance
ITEMS = [
    # ---- avatars ----
    ("avatar 04 composer JW", 4, (11, 105, 56, 149), TEAL, 30),
    ("avatar 04 story card JW", 4, (29.5, 199, 97, 262), TEAL, 30),
    ("plus circle 04 story card", 4, (45, 268, 81, 303.5), TEAL, 30),
    ("avatar 04 story OF (inside ring)", 4, (121, 181, 159, 217), "#2F6B4F", 25),
    ("ring 04 story OF (teal)", 4, (121, 181, 159, 217), TEAL, 25),
    ("avatar 04 post LM", 4, (11, 364.5, 56, 408), "#7A4E7F", 30),
    ("avatar 02 recent login JW", 2, (27, 222, 87, 280.5), TEAL, 30),
    ("camera badge 03", 3, (309.6, 106, 343, 138), TEAL, 30),
    ("dashed circle 03", 3, (262, 75, 348, 142), "#9E9A93", 45),
    ("avatar 05 comment AK", 5, (11, 582, 47, 618), "#7F4552", 30),
    ("avatar 06 AK", 6, (11, 102, 51, 142), "#9B3D4F", 30),
    ("avatar 06 reply LM", 6, (52.5, 201.6, 84.5, 233.7), "#7A4E7F", 30),
    ("avatar 07 JW", 7, (11, 62.6, 62.6, 113.5), TEAL, 30),
    ("avatar 10 JW pill", 10, (32, 718.4, 62.6, 747.5), TEAL, 30),
    ("avatar 11 OF", 11, (14, 28.5, 56, 69), "#2F6B4F", 30),
    ("avatar 12 JW", 12, (14, 28.5, 56, 69), TEAL, 30),
    ("avatar 12 seen-by AK", 12, (11.7, 716, 37, 741), "#9B3D4F", 30),
    ("avatar 13 OF", 13, (11, 142, 66, 196.5), "#2F6B4F", 30),
    ("avatar 13 OP (rounded square)", 13, (11, 411, 66, 465), "#7A4E7F", 30),
    ("avatar 14 SI", 14, (11.7, 188.9, 93.1, 270.3), "#4B4F8E", 30),
    ("mini 14 mutual dot", 14, (99.8, 215.3, 117.3, 232.7), "#4B4F8E", 30),
    ("avatar 15 JW big", 15, (11, 158, 157, 295.8), TEAL, 30),
    ("camera chip 15 avatar", 15, (113.5, 257.6, 149, 291.8), CHIP, 8),
    ("friend tile 15 LM", 15, (11, 698, 121, 777), "#7A4E7F", 30),
    ("avatar 16 JW", 16, (123.7, 97, 235.7, 204), TEAL, 30),
    ("avatar 17 OF big", 17, (106, 145.6, 253.6, 290.7), "#2F6B4F", 30),
    ("ring 17 OF big (teal)", 17, (106, 145.6, 253.6, 290.7), TEAL, 30),
    ("mini 17 mutual AK", 17, (14, 434, 42, 466), "#9B3D4F", 30),
    ("avatar 18 AK", 18, (11, 140.5, 73, 201.6), "#9B3D4F", 30),
    ("type badge 18 love disc", 18, (47.3, 177, 74.3, 204), "#C8384A", 30),
    ("type badge 18 friend disc", 18, (47.3, 250, 74.3, 277), TEAL, 30),
    ("avatar 19 JW", 19, (21.9, 115, 70, 163.4), TEAL, 30),
    ("icon circle 19 help", 19, (16.8, 505.6, 55, 542.8), CHIP, 6),
    ("avatar 20 note AK", 20, (83, 102.3, 142.6, 161), "#9B3D4F", 30),
    ("avatar 20 list AK", 20, (11, 191.5, 70, 249), "#9B3D4F", 30),
    ("online dot 20 list", 20, (52.5, 231.2, 67.7, 246), "#2E9D5A", 30),
    ("group 20 ZR", 20, (13, 271, 55, 312), "#3F6E8C", 30),
    ("group 20 MC", 20, (29.5, 257.6, 70, 295.8), "#6C5B2F", 30),
    ("avatar 21 header AK", 21, (49, 5.6, 93, 50.4), "#9B3D4F", 30),
    ("online dot 21 header", 21, (79.4, 36, 89.6, 46), "#2E9D5A", 30),
    ("avatar 21 big AK", 21, (143, 67.7, 218, 142), "#9B3D4F", 30),
    ("avatar 21 small AK", 21, (8, 311, 40.7, 341.6), "#9B3D4F", 30),
    ("avatar 22 AM (rounded square)", 22, (103, 209, 256, 362), "#7A4E7F", 30),
    # ---- buttons ----
    ("button 02 Log in", 2, (14, 433, 345, 487), TEAL, 30),
    ("button 02 Create new account (outline)", 2, (14, 670, 345, 723.5), TEAL, 40),
    ("button 03 Create account", 3, (14, 555.5, 345, 606.5), TEAL, 30),
    ("button 07 Post", 7, (284, 6.6, 351.3, 46.3), TEAL, 30),
    ("button 13 Join", 13, (286.7, 419, 349.3, 457.7), TEAL, 30),
    ("button 13 See all people (grey)", 13, (11.7, 325.4, 349.3, 367.1), CHIP, 6),
    ("button 14 Confirm", 14, (98.2, 237.8, 221.9, 278.5), TEAL, 30),
    ("button 14 Delete (grey)", 14, (224, 237.8, 347.7, 278.5), CHIP, 6),
    ("button 15 Add to story", 15, (11.7, 386.5, 155.3, 429.7), TEAL, 30),
    ("button 15 Edit profile (grey)", 15, (156.8, 386.5, 299.4, 429.7), CHIP, 6),
    ("button 15 more (grey)", 15, (302, 386.5, 347.8, 429.7), CHIP, 6),
    ("button 17 Add friend", 17, (11.7, 381.4, 160.9, 424), TEAL, 30),
    ("button 18 Confirm", 18, (77.9, 275.4, 192.5, 316), TEAL, 30),
    ("button 18 See previous (grey)", 18, (11.7, 657.3, 349.3, 700.6), CHIP, 6),
    ("button 19 See more (grey)", 19, (11.7, 448.6, 349.3, 493.4), CHIP, 6),
    ("button 19 Log out (grey)", 19, (11.7, 649.7, 349.3, 699), CHIP, 6),
    ("button 08 SELECT MULTIPLE", 8, (190, 306, 350.3, 346.7), TEAL, 30),
    ("button 06 send circle", 6, (308.6, 724.5, 351.3, 766.8), TEAL, 30),
    ("button 10 next circle", 10, (302, 708.3, 351.3, 758.2), TEAL, 30),
    ("button 10 Your story pill", 10, (9, 708.3, 153, 758.2), "#2A2925", 8),
    ("button 09 shutter (white)", 9, (141.5, 576.9, 218, 657.3), WHITE, 8),
    ("button 09 brightness circle", 9, (11.7, 14.8, 56, 60), "#8C9582", 10),
    ("button 08 expand circle", 8, (9, 306, 51, 346.7), "#4A3D2D", 14),
    ("button 13 add friend circle", 13, (304.5, 209.2, 349.3, 254), TINT, 5),
    ("button 15 cover camera", 15, (308.6, 186.4, 347.8, 224.5), CHIP, 8),
    ("button 20 compose circle", 20, (308.6, 5.6, 351.3, 47.4), CHIP, 6),
    ("button 20 your note circle", 20, (15.3, 102.3, 74.3, 161), CHIP, 6),
    ("button 22 control circle", 22, (32, 659.9, 90.6, 718.4), "#2E7579", 8),
    ("button 22 end call", 22, (174.7, 648.2, 256, 728.6), "#C62827", 25),
    ("halo 22 outer", 22, (83, 189, 276.5, 382.4), "#17666A", 3),
    ("halo 22 inner", 22, (83, 189, 276.5, 382.4), "#287278", 3),
    # ---- inputs ----
    ("input 02 email (white)", 2, (16.8, 300, 342.7, 365), WHITE, 5),
    ("input 02 password (white)", 2, (16.8, 366, 342.7, 432), WHITE, 5),
    ("card 02 recent login (white)", 2, (16.8, 205, 342.7, 295), WHITE, 5),
    ("logo tile 02", 2, (141.5, 82, 218, 158), TEAL, 30),
    ("input 03 first name", 3, (16.8, 140, 177, 205), WHITE, 6),
    ("input 03 day", 3, (16.8, 230, 122, 295), WHITE, 6),
    ("input 03 gender female", 3, (16.8, 320, 122, 375), WHITE, 6),
    ("input 03 gender male (teal border)", 3, (126, 320, 233, 375), TEAL, 40),
    ("progress 03 step bar", 3, (16.8, 46.3, 126.3, 54), TEAL, 30),
    ("checkbox 03", 3, (16.8, 528.5, 38, 549.4), TEAL, 30),
    ("input 04 composer pill (border)", 4, (60, 106.4, 302, 148), "#D1D1CF", 18),
    ("input 06 reply", 6, (52.5, 724.5, 308.6, 766.8), CHIP, 6),
    ("input 13 search", 13, (44.8, 3, 347.8, 50.4), CHIP, 6),
    ("input 20 search", 20, (11.7, 52.4, 349.3, 96.2), CHIP, 6),
    ("input 21 Aa", 21, (160.9, 722.5, 315.7, 765.3), CHIP, 6),
    # ---- chips ----
    ("chip 06 Most relevant", 6, (229, 5, 347.8, 46.3), CHIP, 6),
    ("chip 07 Public (tint)", 7, (69, 89.6, 155.3, 120), TINT, 6),
    ("chip 13 All (tint)", 13, (11.7, 54.5, 59, 92), TINT, 5),
    ("chip 13 People", 13, (60, 54.5, 131.4, 92), CHIP, 6),
    ("chip 14 Suggestions", 14, (13.2, 105.4, 118.6, 145.1), CHIP, 6),
    ("chip 15 Posts tab (tint)", 15, (11.7, 435.8, 76.4, 475), TINT, 5),
    ("chip 23 Sell", 23, (13.2, 105.4, 178.2, 145), CHIP, 6),
    ("label 23 JUST LISTED", 23, (19.3, 199, 103.3, 222), "#B84A2A", 25),
    ("tooltip 05 Love", 5, (69, 380, 117, 407), "#1C1B19", 25),
    # ---- cards, bubbles, photos ----
    ("card 19 profile (white)", 19, (11.7, 100, 349.3, 176), WHITE, 4),
    ("card 19 memories (white)", 19, (11.7, 200, 179.7, 290), WHITE, 4),
    ("tray 05 reactions (white)", 5, (11, 423, 307, 479), WHITE, 6),
    ("reaction 05 like", 5, (24.4, 433.3, 62.6, 470), TEAL, 30),
    ("reaction 05 love (raised)", 5, (67.7, 409.3, 118.6, 460.2), "#C8384A", 30),
    ("reaction 11 like", 11, (214.4, 714.3, 251, 750.4), TEAL, 30),
    ("bubble 06 comment", 6, (53.5, 102.3, 347.8, 174.6), CHIP, 6),
    ("bubble 21 received", 21, (42.2, 233.7, 294.3, 271.4), CHIP, 6),
    ("bubble 21 sent", 21, (233, 347.8, 351.3, 387.5), TEAL, 30),
    ("bubble 21 typing", 21, (42.2, 667.5, 99.8, 702), CHIP, 6),
    ("photo 21 chat (lilac sky)", 21, (161.9, 517.3, 351.3, 651.2), "#D8C7D9", 8),
    ("photo 04 story card OF (night)", 4, (116, 173.6, 217, 340.6), "#2E3A4A", 12),
    ("photo 15 cover (teal sky)", 15, (0, 51.4, 360, 235.7), "#BFD7D9", 6),
    ("photo 16 cover (teal sky)", 16, (13.2, 242.4, 347.8, 357), "#BFD7D9", 6),
    ("photo 17 grid night", 17, (13.2, 619.2, 125.3, 728.6), "#2E3A4A", 12),
    ("photo 23 tile (sage sky)", 23, (13.2, 191.5, 178.2, 357), "#CDDAC0", 8),
    ("sheet 07 handle", 7, (150, 436, 210, 448), "#D6D0C9", 20),
    ("band 04 section gap", 4, (0, 150, 360, 175), "#E6E3DA", 5),
    ("band 18 highlight", 18, (0, 128, 360, 330), TINT, 5),
    ("underline 08 tab", 8, (0, 720, 180, 730), TEAL, 30),
    ("badge 08 selection 1", 8, (59, 363.6, 84.5, 387.5), TEAL, 30),
    ("unread dot 20", 20, (331, 211.8, 347.8, 227), TEAL, 30),
    ("icon 04 composer image", 4, (314.7, 117.6, 337.6, 138), TEAL, 40),
]

if __name__ == "__main__":
    cache = {}
    for label, n, box, colour, tol in ITEMS:
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
            print("%-42s no match" % label)
            continue
        bx0, by0 = px.to_dp(n, xs.min() + x0, ys.min() + y0)
        bx1, by1 = px.to_dp(n, xs.max() + 1 + x0, ys.max() + 1 + y0)
        print("%-42s %5.1f x %5.1f dp   at x %5.1f-%5.1f  y %5.1f-%5.1f"
              % (label, bx1 - bx0, by1 - by0, bx0, bx1, by0, by1))
