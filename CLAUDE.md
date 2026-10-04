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

## Responsive rules (phones only)

Follow these in every screen. Tablets and landscape are out of scope; the app is portrait phones only.

- Design baseline is 360dp wide. Never hardcode a screen width in dp. Use match_parent,
  layout_weight and wrap_content so layouts stretch cleanly on phones from 320dp to 430dp wide.
- Fixed dp sizes only for things that should stay the same physical size: icons, avatars,
  button and input heights, badges, corner radii.
- Every screen has a scrolling body (ScrollView) with the top bar and any bottom bar pinned.
- Photos use scaleType centerCrop inside weighted or fixed-ratio containers, never fixed pixel widths.
- Text sizes in sp. Long text wraps or uses maxLines plus ellipsize.
- Handle the status bar and gesture bar with android:fitsSystemWindows="true" on each screen root,
  keeping the design's background colour behind the system bars.
- Lock the app to portrait with android:screenOrientation="portrait" on every Activity in
  AndroidManifest.xml.
- Test target: a 360x800dp emulator for pixel matching, plus one other phone size for the
  complex screens.

## Scope: UI only

Follow these in every screen.

- This assignment is UI only. No backend, database, network, authentication logic, data models,
  ViewModels, Retrofit, Room or permission requests.
- All content is static sample text and the drawables already in res/drawable, copied from the
  PDF screens.
- Kotlin is limited to: starting activities with Intents, finish(), back handling, the log out
  flag, and tiny UI toggles that XML cannot do (show or hide the password, switch the selected
  tab or chip). Keep each Activity as short as possible.
- Buttons that do not lead to another screen in the navigation flow do nothing (no toasts, no
  fake logic), unless the design shows a visual state change XML alone can do.
- Camera, photo picker, voice call and chat are visual screens only. Do not use the camera,
  microphone, storage or any real device API.
- Prefer XML-only solutions (selectors, styles, android:visibility, android:rotation) over
  Kotlin, because the marks for "simple widgets" reward XML without Kotlin code.

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

- On Windows the Bash tool can hang. Run builds and scripts through PowerShell (.\gradlew.bat assembleDebug, python script.py), and never use heredocs (<<'EOF'); write the script to a file first.

## After every screen

1. Build with gradlew.bat assembleDebug (Command Prompt) and fix errors.

2. Tick the screen in docs/PROGRESS.md.

3. git commit with a meaningful message ("feat: add Login screen ..."), then git push.

