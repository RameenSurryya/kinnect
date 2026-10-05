# Icons

Source: Phosphor Icons "Regular" (rounded outline, closest to the design).

URL pattern: https://raw.githubusercontent.com/phosphor-icons/core/main/assets/regular/<name>.svg

Names below are suggestions. If one 404s, pick the nearest on phosphoricons.com and update this file.

Tabs/top bar: ic_home=house, ic_friends=hand-drawn (see Custom; Phosphor users had two full figures), ic_store=storefront, ic_bell=bell, ic_menu=list,

ic_search=magnifying-glass, ic_messenger=hand-drawn (see Custom; chat-circle had no bolt)

Post/feed: ic_image=image, ic_tag=tag, ic_smile=smiley, ic_pin=map-pin, ic_live=video-camera,

ic_camera=camera, ic_calendar=calendar-blank, ic_like=thumbs-up, ic_comment=chat (tail bottom-left as in 04/05; was chat-centered),

ic_share=arrow-bend-up-right, ic_globe=globe, ic_close=x, ic_more=dots-three, ic_back=caret-left,

ic_chevron_down=caret-down, ic_chevron_right=caret-right, ic_eye=eye, ic_info=info,

ic_plus_circle=plus-circle, ic_check=check, ic_expand=corners-out, ic_select_multiple=copy

People/profile: ic_add_person=user-plus, ic_person=user, ic_groups=users-three,

ic_briefcase=briefcase, ic_graduation=graduation-cap, ic_clock=clock, ic_edit=pencil-simple,

ic_bookmark=bookmark-simple

Camera/story: ic_flash=lightning, ic_flip=camera-rotate, ic_star=star, ic_send=paper-plane-tilt,

ic_heart=heart, ic_text_aa=text-aa, ic_music=music-notes, ic_sparkle=sparkle, ic_brightness=sun,

ic_create_reel=hand-drawn (see Custom; film-slate had no play triangle)

Chat/call: ic_phone=phone, ic_video=video-camera, ic_mic=microphone, ic_call_end=phone-disconnect,

ic_speaker=speaker-high, ic_transcript=article

Menu: ic_logout=sign-out, ic_help=question, ic_settings=sun, ic_apps=squares-four, ic_memories=clock-counter-clockwise

Added after checking the screens: ic_lock=lock ("End-to-end encrypted", screen 22),
ic_plus=plus (white "+" on the Create story card, screen 04).
Filled variants (Phosphor Fill): ic_like_filled=thumbs-up-fill, ic_heart_filled=heart-fill.
No ic_home_filled: the active tab in the design is still an outline icon (teal).
All names above resolved on Phosphor with no 404s. SVG sources are in design/svg/.
design/svg/map.txt lists the same mapping (icon name, Phosphor name); "custom" means hand-drawn.

## Custom (hand-drawn VectorDrawables from the PNGs, no download)

Checked against the design with tools/check_glyphs.py (side-by-side sheets in design/check/).
Colours are literal hex values sampled from the PNGs.

Re-drawn icons (black, tint with app:tint, 256 viewport, 16-unit round strokes like Phosphor):

- ic_messenger: round bubble, tail pointing down at bottom-left, zigzag bolt rising left to right (04, 18, 20).
- ic_create_reel: clapperboard with a play triangle ("Create" in 12, "Stories" tab in 20).
- ic_friends: a person in front (ring head, arched shoulders) and the right half of a second
  person behind (C-shaped head, one shoulder); 20-unit strokes, slightly heavier than Phosphor's 16
  (Friends tab in 04/14/18/19/23, Groups shortcut in 19). Measured 20.5 x 17.0 dp on the emulator
  vs 20.4 x 17.3 dp in the design.

Logo (viewport 100, three equal rings: stroke = 0.32 x radius, bottom rings 0.57 x radius left/right
and 1.0 x radius below the top ring, fitted to design/logo.png):

- logo_kinnect: white #FFFFFF (tint grey for the Login footer).
- logo_kinnect_teal: teal #0B5F63.

Reactions (viewport 64, disc fills it, white glyph, default 32dp):

- reaction_like #0B5F63 (sampled #0D5E62, same as primary), reaction_love #C8384A,
  reaction_haha / reaction_wow / reaction_sad #C98714, reaction_angry #B74A2B.
- No *_small variants: the small reactions in 04/06, the buttons in 11, the floating hearts in 12,
  the heart on the bubble in 21, the heart after the name in 22 and the heart/like badges in 18 are
  the same glyphs. Size, opacity (12) and the white separator ring (04/06/18/21) are layout properties.

Notification type badges for screen 18 (viewport 64, coloured disc + white glyph, default 20dp;
the white ring around them is a layout background):

- badge_friend_request #0B5F63 (person, hand-drawn), badge_comment #2B6D4F (Phosphor Bold chat),
  badge_group #4B4F8E (two people, hand-drawn), badge_tag #C98714 (Phosphor Bold tag).

## Photo placeholders (ph_*)

ph_sand, ph_teal, ph_lilac, ph_sky, ph_sage, ph_rose, ph_night: flat sky, pale sun, back hill,
front hill. Colours per family are in DESIGN_TOKENS.md. All seven share the same shapes.

- Every placeholder in the design (36 frames on 13 screens) is a centre crop of ONE square
  picture, so the viewport is square (360 x 360, default 360dp) and every ImageView uses
  android:scaleType="centerCrop". That alone gives the right crop for each use (table below).
- Shapes measured from all 36 frames with tools/sample_placeholders.py (writes
  design/check/placeholder_geometry.json). Fitted and written by tools/make_placeholders.py:
  sun circle centre (259.4, 108.1) radius 36.0; each hill = 3 smooth cubic curves with the crest
  and trough as knots. The hill ends sit a little outside the viewport (the drawable clips them).
- Checked with tools/check_placeholders.py (sheets design/check/ph_<family>.png: design |
  drawable centre-cropped | overlay). Mean edge offset 0.13 px over all frames, worst 0.92 px
  (09 camera, 1311 px tall).

What centerCrop shows (viewport units, PNG frame 707 px = 360 dp):

| Use | Frame (dp) | Shape | Visible part of the 360 x 360 picture |
|---|---|---|---|
| 10, 11, 12 story; 09 camera | 344 x 680 (09: 344 x 668) | tall 0.51 | x 89-271, full height; sun cut by the right edge |
| 04 story card | 95 x 161 | tall 0.59 | x 74-286 |
| 04 large post photo (05 too) | 178 x 238 | tall 0.75 | x 46-314 |
| 08 grid, 17 photos, 23 tiles, 09 gallery thumb | 88 / 106 / 160 / ~36 square | 1.0 | whole picture |
| 08 preview | 359 x 303 | wide 1.19 | y 28-332 |
| 21 chat photo, 06 comment photo | 184 x 127, 164 x 113 | wide 1.45 | y 55-305 |
| 04 small post tiles | 177 x 117 | wide 1.52 | y 62-298 |
| 15, 17 cover | 359 x 179 | wide 2.0 | y 90-270; sun cut by the top edge |
| 16 cover | 329 x 109 | wide 3.0 | y 120-240; only the bottom of the sun shows |

Overlays (the dark "+4" layer, 04 story name scrim, 08 selection rings, "0:23" label) are layout
views on top, not part of the drawables.

Icon sizes are in DESIGN_TOKENS.md (Sizes): 24 dp default, Home tab 25 dp, top bar 19 / 15 dp,
composer image icon 21 dp.
