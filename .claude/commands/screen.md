---

description: Build one Kinnect screen from its design PNG

argument-hint: <number> <Name>   e.g. 04 Home feed

---

Build screen $ARGUMENTS.

1. Read CLAUDE.md and the row for this screen in docs/SCREENS.md.

2. Open the matching design/screens/screen-NN.png and study it closely: spacing, corner radii,

   font sizes and weights, colours, icon sizes, and every overlapping element.

3. Create the Activity and layout using only the allowed basic layouts. Use existing tokens and

   styles; add new ones to the values files if missing. Use only icons already in res/drawable.

4. Register it in AndroidManifest.xml and wire the navigation exactly as in SCREENS.md.

5. Build, fix errors, update docs/PROGRESS.md, commit and push.

6. Finish with a short list of anything that differs from the PNG or needed an ADVANCED concept.

