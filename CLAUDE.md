# Kinnect – rules for Claude Code

Android app (package com.rameen.kinnect). 23 screens copied from design/screens/screen-NN.png.

Read first: @docs/SCREENS.md @docs/DESIGN_TOKENS.md @docs/ICONS.md @docs/PROGRESS.md

## Stack

- Kotlin + XML Views, ViewBinding. One Activity per screen. Basic layouts only.

- Packages: ui/auth, ui/home, ui/social, ui/profile, ui/chat, ui/market (see SCREENS.md).

- Never edit anything inside design/.

## Layout rules (try earlier options first)

1. LinearLayout (layout_weight for columns) is the default.

2. FrameLayout for anything that overlaps (badges, "+4" over a photo, dim overlays).

3. RelativeLayout for simple positioning (top bars).

4. GridLayout for true grids (photo picker, marketplace, shortcuts).

5. ScrollView / HorizontalScrollView with static sample content. No RecyclerView unless truly needed.

6. Basic widgets only: TextView, ImageView, Button, EditText, CheckBox, RadioGroup, Spinner, ProgressBar, View.

7. Styling via drawable shapes and styles.xml. No custom views, no layout libraries.

8. Rotation: android:rotation. Enlarging: scaleX/scaleY.

## Advanced concepts

Before using ConstraintLayout, RecyclerView, animations or custom drawing: STOP and tell me

the screen, the element, why basic XML cannot do it, and what you propose.

Mark it in XML with <!-- ADVANCED: reason -->.

## Naming

- Activity: XxxActivity. Layout: activity_xxx.xml. Included layouts: include_xxx.xml.

- View ids snake_case with prefix: btn_, tv_, iv_, et_, ll_, fl_, rg_ (e.g. btn_login).

- Drawables: ic_ (icons), bg_ (shapes), ph_ (vector photo placeholders), photo_ (real photos).

- All visible text in strings.xml. All colours/sizes in colors.xml / dimens.xml / styles.xml.

## Icons and images

- Icons are VectorDrawables in res/drawable, tinted with app:tint. Never invent a substitute: if an

  icon is missing, add it to docs/ICONS.md and tell me.

- Real photos go in res/drawable-nodpi (JPG, under 300 KB each). Initials avatars stay as styled TextViews.

## Navigation

- Explicit Intents. Back must return to the previous screen.

- Splash and Login call finish() after moving on.

- Top tabs use FLAG_ACTIVITY_REORDER_TO_FRONT so they don't pile up.

- Log out: FLAG_ACTIVITY_NEW_TASK or FLAG_ACTIVITY_CLEAR_TASK to LoginActivity.

## Quality

- Scrollable roots, 48dp minimum touch targets, contentDescription on icon buttons, readable contrast.

- Comment the code clearly: the author must explain it in a live demo. Keep code simple.

## After every screen

1. Build with gradlew.bat assembleDebug (Command Prompt) and fix errors.

2. Tick the screen in docs/PROGRESS.md.

3. git commit with a meaningful message ("feat: add Login screen ..."), then git push.

