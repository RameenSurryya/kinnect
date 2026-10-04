# Icons

Source: Phosphor Icons "Regular" (rounded outline, closest to the design).

URL pattern: https://raw.githubusercontent.com/phosphor-icons/core/main/assets/regular/<name>.svg

Names below are suggestions. If one 404s, pick the nearest on phosphoricons.com and update this file.

Tabs/top bar: ic_home=house, ic_friends=users, ic_store=storefront, ic_bell=bell, ic_menu=list,

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

Added after checking the screens: ic_lock=lock ("End-to-end encrypted", screen 22).
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

Still to do: ph_* sun-and-hills placeholders in each palette.

