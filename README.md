# i230806 – Kinnect

Kinnect is a social networking app UI for Android (package `com.rameen.i230806`). It recreates
23 screens from the design PDF (`design/Kinnect_UI.pdf`, one PNG per screen in
`design/screens/`): sign in, a feed with stories and reactions, friends, profiles, notifications,
chat, a voice call and a marketplace. It is **UI only**: all content is static sample text and
drawables, with no backend, database or network code.

## Build and run

Requirements: Android Studio (recent stable) with Android SDK 37. Gradle downloads the JDK it
needs (25) on first build. Min SDK 26.

- **Android Studio:** File > Open > select this folder, wait for Gradle sync, choose the `app`
  run configuration and press Run on a phone emulator (a 360 x 800 dp phone matches the design).
- **Command line (Windows PowerShell):**
  ```
  .\gradlew.bat assembleDebug        # APK in app\build\outputs\apk\debug\
  .\gradlew.bat installDebug         # install on the running emulator or phone
  ```

The app is locked to portrait and designed for phones from 320 to 430 dp wide.

## Screens and navigation

Splash (2 s) opens Login. **Log in** opens Home; **Create new account** opens Sign up.
Home, Friends, Notifications, Menu and Marketplace share a five-tab top bar.

| # | Screen | Reached from / leads to |
|---|---|---|
| 01–03 | Splash, Login, Sign up | Splash and Login finish() after moving on |
| 04 | Home feed | Search, Chats, Create post, Comments, Reaction picker (long-press Like), Story viewer, Camera, Profile |
| 05–06 | Reaction picker, Comments | back to Home |
| 07–08 | Create post, Photo picker | Photo/video → Photo picker → Next → Create post |
| 09–12 | Camera, Story editor, Story viewer, Your story | shutter → editor → Your story → X → Home |
| 13 | Search | person result → Other profile |
| 14, 18 | Friends, Notifications | a request → Other profile |
| 15–17 | Profile, Edit profile, Other profile | Edit profile ↔ Profile; Message → Chat |
| 19 | Menu | profile card → Profile; shortcuts; **Log out** → Login with the back stack cleared |
| 20–22 | Chats, Chat, Voice call | row → Chat → phone icon → Voice call → end call → Chat |
| 23 | Marketplace | tabs only |

Back always returns to the previous screen. Tabs use `FLAG_ACTIVITY_REORDER_TO_FRONT` so they
do not pile up. The full table is in `docs/SCREENS.md`.

## Package structure

```
app/src/main/java/com/rameen/i230806/
  ui/BaseActivity.kt      shared parent: edge-to-edge bars, top bar + tab bar wiring
  ui/auth/                Splash, Login, SignUp
  ui/home/                Home, ReactionPicker, Comments, CreatePost, PhotoPicker, Camera,
                          StoryEditor, StoryViewer, YourStory, Search
  ui/social/              Friends, Notifications, Menu
  ui/profile/             Profile, EditProfile, OtherProfile
  ui/chat/                Chats, Chat, VoiceCall
  ui/market/              Marketplace
app/src/main/res/layout/  activity_*.xml (one per screen), include_top_bar.xml, include_top_tabs.xml
app/src/androidTest/java/com/rameen/i230806/   the two Espresso tests
```

## Design decisions

- **One Activity per screen, XML Views with ViewBinding.** Layouts use only basic containers
  (LinearLayout with weights, FrameLayout for overlaps such as badges and the "+4" photo,
  RelativeLayout, GridLayout, ScrollView) and basic widgets. No RecyclerView or custom views.
- **XML first.** Styling is done with drawable shapes, selectors and `styles.xml`; Kotlin only
  starts activities, handles back and log out, and toggles small UI states (password eye,
  selected tab or chip). Each Activity is kept short and commented.
- **Design tokens.** Every colour, size and text style was measured from the PNGs (1 dp =
  1.964 PNG px) and lives in `colors.xml`, `dimens.xml` and `styles.xml`. `docs/DESIGN_TOKENS.md`
  documents each value and where it was sampled.
- **Fonts.** Headings use Bricolage Grotesque (Bold / ExtraBold), body text uses Figtree. Both
  were chosen by scoring candidates against the design text and are bundled as static TTFs in
  `res/font` (SIL Open Font License, see `docs/licenses/`), so text renders correctly offline.
- **Icons and photos.** Icons are Phosphor "Regular" VectorDrawables, plus a few hand-drawn ones
  (messenger, friends, create reel, logo, reactions). Every photo in the design is the same
  sun-and-hills placeholder in seven colours, redrawn as `ph_*` vectors shown with `centerCrop`.
  See `docs/ICONS.md`.
- **Responsive.** 360 dp baseline, no hardcoded widths, scrolling bodies with pinned bars,
  `fitsSystemWindows` on each root, 48 dp touch targets and content descriptions on icon buttons.

## tools/ scripts (Python, used while building; not part of the app)

| Script | What it did |
|---|---|
| `px.py` | Measures the design PNGs in dp: scale, colour runs, bounding boxes, zoomed crops |
| `sample_colors.py` | Sampled every colour token as a median over many pixels |
| `measure_dims.py` | Measured sizes of avatars, buttons, inputs, chips, cards and bars |
| `measure_radii.py` | Fitted corner radii from each corner's edge profile |
| `measure_text.py` | Solved text sizes in sp from rendered ink boxes |
| `compare_fonts.py` | Scored candidate Google Fonts against design text crops |
| `make_fonts.py` | Built the bundled static font files from the variable fonts |
| `sample_placeholders.py` | Measured the placeholder scene's geometry and colours across all frames |
| `make_placeholders.py` | Wrote the seven `ph_*` placeholder VectorDrawables |
| `check_placeholders.py`, `check_glyphs.py` | Compared placeholders and hand-drawn icons with the design |

Run them from the project root, for example `python tools\px.py`. They need Pillow, NumPy and SciPy
(`fonttools` and PyMuPDF for the font and glyph scripts).

## Espresso tests

Start an emulator (or connect a phone), then run:

```
.\gradlew.bat connectedDebugAndroidTest
```

- `HomeToCommentsTest`: opens Home, scrolls to a post, taps **Comment**, checks the Comments
  screen, presses Back and checks Home is showing again.
- `LoginLogoutBackStackTest`: Login → Home → Menu → **Log out** → Login, then presses Back and
  checks the app closes (log out cleared the back stack).

Results: `app\build\reports\androidTests\connected\debug\index.html`. Animations are turned off for
the test run in `app/build.gradle.kts`.
