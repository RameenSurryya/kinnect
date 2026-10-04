# Design tokens

All values below were measured from design/screens/*.png with the scripts in tools/ (run them
from the project root through PowerShell). They are the source for res/values/colors.xml,
dimens.xml and styles.xml.

| Script | Measures |
|---|---|
| tools/px.py | the scale; colour runs along a line, raw pixels, bounding boxes, zoomed crops (all in dp) |
| tools/sample_colors.py | every colour token (median of many pixels) |
| tools/measure_dims.py | sizes of avatars, buttons, inputs, chips, cards, bars |
| tools/measure_radii.py | corner radii (fits a circle to each corner's edge profile) |
| tools/compare_fonts.py | font choice (renders candidates over design crops, scores the overlap) |
| tools/measure_text.py | text sizes in sp |

## Scale

**1 dp = 1.964 PNG px (707 px = 360 dp). Screen origin = PNG pixel (62, 89).**

Method: every PNG is 831 x 1806 with the phone screen drawn inside a thin grey outline
(#CFCAC1). `python tools/px.py raw` across the outline shows it centred on x = 61.3 and
x = 768.3 and on y = 88.0 and y = 1615.5, so the screen is 707 x 1527 px. Taking the width as
the 360 dp design baseline gives 1.964 px per dp, and the height comes out at 777.6 dp: exactly
a 360 x 800 dp phone minus its 24 dp status bar (the design does not draw the status bar).

Confirmed against known elements:

- Tabs: the five tab columns and the active-tab underline are 72 dp wide (360 / 5).
- Tab bar: 48 dp from the top-bar row to the divider; the 24 dp tab icons sit centred in it.
- Phosphor icons drawn at 24 dp: the house glyph measures 19.3 dp (expected 19.5 dp).
- Round numbers everywhere else: 36 dp circles, 44 dp primary buttons, 48 dp search avatars,
  72 dp end-call button, 144 dp call avatar.

Screen 14's frame is drawn 17 px left and 8 px up of the others; tools/px.py corrects for it.
The PNGs carry slight compression noise (a flat teal reads #0B5F63 +/- 3), so colours are
always medians over many pixels, never single pixels.

## Colours

Sampled with tools/sample_colors.py. Repeat samples of the same token agreed within 2 units
per channel; where an existing drawable already used a sampled value (reactions, badges)
that value is kept.

| Token (colors.xml) | Value | Sampled from |
|---|---|---|
| teal | #0B5F63 | Log in button (02), tab underline (04), Confirm (14), send circle (06) |
| teal_tint | #E3EFEF | "All" chip (13), "New" band (18), add-friend circle (13), Posts tab (15) |
| background | #F3F2EE | login (02), sign up (03), menu (19) |
| surface | #FFFFFF | feed and list screens, cards, inputs |
| chip_fill | #ECE9E2 | top bar circles (04), chips (13, 14), See more (19), search (13, 20), bubbles (06, 21: #EDEAE3) |
| divider | #E0E0DE | under the tab bar (04), between sections (14), above Like row (04) |
| border | #D6D1C8 | input and card outlines (02, 03; 1 PNG px = 0.5 dp) |
| section_band | #E6E3DA | thick gaps in the feed (04) |
| track | #D6D0C9 | empty step bar and password meter (03: #D5D0CA / #D7D0C9), sheet handle (07) |
| card_shadow | #E8E6E2 | soft line under the menu cards (19) |
| text_dark | #1C1B19 | names and body text (04, 14, 02), black swatch (07) |
| text_grey | #5B5954 | subtitles, times, labels, inactive tab icons (#5C5D58) |
| text_hint | #74726E | placeholders: Search (20), Write a reply (06), Aa (21), Website (16) |
| text_on_teal_soft | white 80 % | "from" (01), call timer and "End-to-end encrypted" (22) |
| accent_orange | #B84A2A | badges (04, 02), JUST LISTED (23), swatch (07: #BA4929), angry (05), meter (03) |
| love_red | #C8384A | love reaction (05: #C9374A) |
| mustard | #C98714 | haha reaction and swatch (05, 07: #C98611) |
| purple | #7A4E7F | swatch (07), LM / BA / OP / AM avatars |
| indigo | #4B4F8E | swatch (07), SI / OS avatars |
| green | #2F6B4F | swatch (07), OF / NF avatars |
| online_green | #2E9D5A | online dots (20), close-friends star circle (10) |
| maroon | #9B3D4F | AK / DS avatars, unread dot (20) |
| steel_blue | #3F6E8C | ZR avatar |
| olive | #6C5B2F | DC / MC avatars |
| brown | #8A5A2C | HA / OT avatars |
| camera_bg | #121212 | camera, story editor, story viewer, your story (09-12) |
| story_pill | #2A2925 | Your story / Close friends pills (10) |
| photo_button_light | black 32 % | camera top buttons over the sage photo (09): #8C9582 over #CDDAC0 |
| photo_button | black 40 % | story editor buttons (10): #798172 over #CDDAC0 |
| photo_button_dark | black 50 % | expand button (08): #4A3D2D over #9E7B55 |
| overlay_dim | #1C1B19 at 36 % | whole-screen dim (05): white reads #ACABA7 |
| call_control | white 14 % | call buttons on teal (22): #2E7579 |
| call_halo_outer / inner | white 5 % / 12 % | rings around the call avatar (22): #17666A / #287278 |
| call_end_red | #C62827 | end-call button (22) |

Translucent tokens were fitted by solving `photo x (1 - a) + layer x a = measured` per channel;
all three channels agreed within 1 %.

Initials avatars use eight disc colours (white bold initials on top):

| Colour | People (colors.xml alias) |
|---|---|
| teal | JW |
| purple | LM, BA, OP (group, rounded square), AM (rounded square) |
| maroon | AK, DS |
| indigo | SI, OS |
| green | OF, NF |
| brown | HA, OT |
| steel_blue | ZR |
| olive | MC, DC |

## Sizes (dp)

Measured with tools/measure_dims.py (bounding boxes add up to ~0.5 dp of anti-aliasing, so
values are rounded down to whole dp).

- Margins: 16 dp on most screens; 20 dp on login and sign up (02, 03).
- Top bar (04): row 49 dp; title or wordmark centred vertically, 16 dp from the left;
  search and messenger circles 36 dp, 8 dp apart, 16 dp from the right edge, icons 19 dp;
  messenger badge 18 dp (14 dp red disc + 2 dp white ring), centre 12 dp right and 13 dp above
  the circle centre.
- Tab bar: 48 dp, five equal columns, 24 dp icons, 3 dp teal underline the full column width,
  1 dp divider under the bar. Bell badge centre 13 dp right and 7 dp above the tab centre.
- Toolbars with a back arrow: 52 dp (03, 05-08, 13, 15-17), chat header 56 dp (21).
  Bottom nav (20): 56 dp.
- Avatars (every size in the design): 20, 24, 26, 30, 33, 35, 36, 40, 44, 48, 52, 55, 58, 66,
  74, 103, 130 (+4 dp white ring), 144. Story ring (04): 38 dp outside, 1.5 dp teal + 1.5 dp
  white around the disc. Profile ring (17): 3 dp teal + 3.5 dp white.
- Icons: 24 dp default (tabs), 19 dp in the top bar circles, 16 dp in chips, 12 dp globe.
  Reactions 32 dp (05 tray and 11; measured 32.1 and 31.6), hovered reaction 46 dp, small
  summary reactions 18 dp. Badges 18 dp. Notification type badges 20 dp + 2 dp ring.
  Online dot 8 dp + ring, unread dot 11 dp.
- Buttons: primary pill 44 dp (02, 03, 10); outline 46 dp (02); medium 37 dp (Add to story,
  Edit profile, See more, See previous, SELECT MULTIPLE); small 35 dp (Confirm / Delete in 14,
  See all people); 33 dp (Confirm / Delete in 18, Post); Join 31 dp; Log out 41 dp;
  circle buttons 36 dp (send, compose, add friend), next arrow 44 dp; menu row icon circle 33 dp.
- Inputs: 50 dp (with floating label), 54 dp (password with eye), 37 dp search / reply / Aa,
  gender options 44 dp.
- Chips: 33 dp (14, 15), 31 dp (13 filters), 35 dp (23 Sell / Categories), 24 dp (07 Public).
- Section band 7 dp (04). Dividers 1 dp; input and card outlines 0.5 dp.

Corner radii (tools/measure_radii.py):

| Radius | Used by |
|---|---|
| pill | primary and outline buttons, chips, search fields, reaction tray, tooltip, SELECT MULTIPLE |
| 4 dp | joined corners of grouped chat bubbles (21) |
| 6 dp | JUST LISTED (6.4), profile photo grid (6.7), camera gallery thumb (5.3) |
| 10 dp | Confirm / Delete / Join / See more / Log out / Add to story (9.5-11.2), colour swatches |
| 12 dp | inputs (11.5-12.0), menu cards (12.2-13.1), story cards (12.6), product tiles (11.7), friend tiles (11.8), 48 dp group avatar (12.5) |
| 14 dp | recent login card (02) |
| 16 dp | camera / story frame (09-12) |
| 18 dp | comment bubble (17.9), chat bubbles, chat photo (18.8) |
| 20 dp | bottom sheet top corners (07, estimated: white on white) |
| 21 dp | teal app tile on login (02) |
| 26 dp | end-call button (22) |
| 44 dp | 144 dp call avatar (22) |

## Fonts

**Headings: Bricolage Grotesque Bold (700); wordmark and profile names: ExtraBold (800).
Everything else: Figtree (Regular 400, Medium 500, SemiBold 600, Bold 700).**
Both are downloadable Google Fonts (res/font/*.xml, fetched by Google Play services; the
certificates in res/values/font_certs.xml come from Google's DownloadableFonts sample and the
fonts are preloaded via manifest meta-data).

Evidence (tools/compare_fonts.py; sheets in design/check/font_*.png). Each candidate was
rendered with the same text, scaled onto the design crop's ink box and scored by overlap
(IoU, 1.0 = identical):

| Sample | Best | Runner-up |
|---|---|---|
| "What's your name and" (03) | Bricolage Grotesque 700: 0.854 | Schibsted Grotesk 700: 0.680 |
| "birthday?" (03) | Bricolage Grotesque 800: 0.836 | Sora 800: 0.658 |
| "kinnect" wordmark (04) | Bricolage Grotesque 800: 0.838 | Hanken Grotesk 800: 0.777 |
| "Notifications" (18) | Bricolage Grotesque 700: 0.826 | Funnel Display 700: 0.793 |
| "Jacob West" profile name (15) | Bricolage Grotesque 800: 0.893 | Funnel Display 700: 0.768 |
| "What's on your mind, Jacob?" (04) | Figtree 500: 0.620 | DM Sans 500: 0.604 |
| "Tap to log in" (02) | Figtree 400: 0.789 | Plus Jakarta Sans 500: 0.726 |
| "Log in" button (02) | Figtree 700: 0.882 | Onest 700: 0.859 |
| "Lina Marsh" (04) | Onest 700: 0.841 | Figtree 600: 0.827 |
| "Saved" (19) | Albert Sans 500: 0.824 | Figtree 500: 0.745 |

Bricolage Grotesque wins every heading sample by a wide margin and has the design's tell-tale
glyphs (the u-shaped "y", the curved leg of "K" and "k"). Figtree wins or comes second on every
body sample except the 51-character post line, where small spacing differences add up; it also
matches the single-storey "g" and straight-tailed "y". Optical size barely matters for
Bricolage (opsz 14 to 48 changes the score by under 0.02), so the provider's default instance
is fine.

Candidates tried: headings — Bricolage Grotesque, Familjen Grotesk, Schibsted Grotesk,
Gabarito, Instrument Sans, Hanken Grotesk, Onest, Parkinsans, Funnel Display, Host Grotesk,
Rethink Sans, Archivo, Sora; body — Figtree, Albert Sans, Plus Jakarta Sans, DM Sans, Outfit,
Urbanist, Onest, Golos Text, Manrope, Rethink Sans.

Text sizes (tools/measure_text.py, from the ink height and width of each string):

| Style (styles.xml) | Font | Size | Examples |
|---|---|---|---|
| Kinnect.Text.Wordmark | Bricolage 800, teal | 28 sp | kinnect (04) |
| Kinnect.Text.ProfileName | Bricolage 800 | 26 sp | Jacob West (15), Omar Farooq (17) |
| Kinnect.Text.Heading | Bricolage 700 | 24 sp | Friends, Notifications, Menu, Marketplace, Chats, "What's your name and birthday?" |
| Kinnect.Text.Title / SectionTitle | Bricolage 700 | 18 sp | Create account, Comments, Friend requests, Today's picks |
| Kinnect.Text.SectionTitle.Small | Bricolage 700 | 17 sp | New, Earlier, People, Groups |
| Kinnect.Text.Name | Figtree 600 | 15 sp | Sara Iqbal (14), Jacob West (02) |
| Kinnect.Text.Body | Figtree 400 | 14 sp | post text, bubbles |
| Kinnect.Text.Body.Bold | Figtree 600 | 14 sp | Lina Marsh (04) |
| Kinnect.Text.Label | Figtree 600, grey | 13 sp | All shortcuts, RECENT LOGIN |
| Kinnect.Text.Caption | Figtree 400, grey | 12 sp | 8 mutual friends, 2h, field labels |
| buttons | Figtree 700 | 15 sp primary, 14 sp small, 13 sp chips | Log in, Confirm, Suggestions |
| badges, nav labels | Figtree 700 / 600 | 11 sp | badge digits, Chats / People / Stories |
| JUST LISTED | Figtree 700 | 10 sp | (23) |

## Known differences inside the design

- The search / messenger circles are 36 dp on Home (04) but about 31 dp on 14, 18, 19 and 23.
  The shared top bar uses 04's 36 dp (dimen top_bar_button) so every tab looks the same.
- Confirm / Delete are 35 dp tall in 14 and 33 dp in 18; Join is 31 dp (13). Each has a dimen.
- Screens 14, 18, 19 and 23 show a stray light line above the top bar buttons (a leftover in
  the mock-up); it is not reproduced.

## Photo placeholders (sampled exactly)

Sampled from the PNGs with tools/sample_placeholders.py (most frequent exact colours of a clean
frame; the same values appear in every frame of that family). Drawables: res/drawable/ph_<family>.xml.
The same colours are in colors.xml as ph_<family>_sky / _sun / _back / _front.

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
#141414 layer): 04 "+4" tile ~50% (photo_dim), 04 story card name scrim ~42% over the bottom
78 of 316 px (story_scrim), 05 whole-screen dim 36% (overlay_dim, re-fitted above).
