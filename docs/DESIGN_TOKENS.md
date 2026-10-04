# Design tokens

Exact: primary teal #0B5F63.

Approximate (estimated by eye): sample the PNGs with a Pillow script, then replace these

with exact values and note it here.

- screen background (warm off-white) ~#F3F1ED    - chip / input fill ~#ECE9E3

- divider / border ~#D8D4CC                       - text dark ~#1F1F1F, text grey ~#6B665F

- badge / accent orange-red ~#B84A2A              - love red ~#D0384F

- mustard ~#C98A10  - purple ~#7B4F7E  - indigo ~#4B4F94  - green ~#2F6B4F  - online green ~#2E9E5B

Fonts: Figtree for body (Google Fonts, downloadable font). Headings: bold grotesque like the PNGs

(try Bricolage Grotesque); compare visually and record the final choice here.

Shapes: buttons fully rounded; inputs ~14dp radius; cards ~16dp; chips pill; avatars circle;

bottom sheet top corners ~24dp.

Scale: assume each PNG phone frame = 360dp wide, so dp = px × 360 / frame_width_px.

Confirm against one known element and record the scale here.

## Photo placeholders (sampled exactly)

Sampled from the PNGs with tools/sample_placeholders.py (most frequent exact colours of a clean
frame; the same values appear in every frame of that family). Drawables: res/drawable/ph_<family>.xml.

| Family | Sky (background) | Sun | Back hill | Front hill | Screens |
|---|---|---|---|---|---|
| sand | #E9D7BF | #FFF3DD | #C8A57F | #9E7B55 | 04, 05, 08, 23 |
| teal | #BFD7D9 | #F2E3C6 | #7FA9A8 | #4F8585 | 04, 08, 09 (gallery thumb), 15, 16 |
| lilac | #D8C7D9 | #F4D5B8 | #A48AA7 | #6F5673 | 04 ("+4" tile), 08, 17, 21 |
| sky | #CBD8E9 | #F5EBD0 | #8FA8C7 | #5C769B | 06, 08, 17, 23 |
| sage | #CDDAC0 | #F3EBC7 | #93AD7E | #627F4F | 04, 08, 09, 10, 12, 23 |
| rose | #E5C9BD | #FBEBDC | #C68F7B | #955E4A | 04, 08, 23 |
| night | #2E3A4A | #E8C989 | #465670 | #202634 | 04, 08, 11, 17 |

Overlays on top of placeholders (layout, not part of the drawable; fitted as a near-black
#141414 layer, approximate): 04 "+4" tile ~50%, 04 story card name scrim ~42% over the bottom
78 of 316 px, 05 whole-screen dim ~32%.

