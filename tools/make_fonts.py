"""Build the bundled fonts in app/src/main/res/font from the Google Fonts variable fonts.

Downloads Figtree and Bricolage Grotesque (variable TTFs, SIL Open Font License) from
github.com/google/fonts, cuts one static instance per weight with fontTools, and writes them
under the resource names the styles use (figtree_regular.ttf ...). Also saves each font's
OFL.txt to docs/licenses/ (the licence must travel with the fonts).

Bricolage Grotesque also has an optical-size axis; it is fixed at 24, the value that matched
the design best (docs/DESIGN_TOKENS.md, Fonts), and its width axis at the normal 100.

Run from the project root:  python tools/make_fonts.py   (needs fonttools)
"""
import io
import os
import urllib.request

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

RAW = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
SOURCES = {
    "figtree": "figtree/Figtree%5Bwght%5D.ttf",
    "bricolage": "bricolagegrotesque/BricolageGrotesque%5Bopsz%2Cwdth%2Cwght%5D.ttf",
}
LICENCES = {
    "Figtree": "figtree/OFL.txt",
    "BricolageGrotesque": "bricolagegrotesque/OFL.txt",
}
# resource name -> (source, axis values)
INSTANCES = {
    "figtree_regular": ("figtree", {"wght": 400}),
    "figtree_medium": ("figtree", {"wght": 500}),
    "figtree_semibold": ("figtree", {"wght": 600}),
    "figtree_bold": ("figtree", {"wght": 700}),
    "bricolage_grotesque_bold": ("bricolage", {"wght": 700, "opsz": 24, "wdth": 100}),
    "bricolage_grotesque_extrabold": ("bricolage", {"wght": 800, "opsz": 24, "wdth": 100}),
}
OUT = "app/src/main/res/font"


def fetch(path):
    with urllib.request.urlopen(RAW + path, timeout=60) as r:
        return r.read()


if __name__ == "__main__":
    data = {key: fetch(path) for key, path in SOURCES.items()}
    for name, (src, axes) in INSTANCES.items():
        font = TTFont(io.BytesIO(data[src]))
        static = instancer.instantiateVariableFont(font, axes)
        path = os.path.join(OUT, name + ".ttf")
        static.save(path)
        print("%-32s %s  %d KB" % (path, axes, os.path.getsize(path) // 1024))
    os.makedirs("docs/licenses", exist_ok=True)
    for name, path in LICENCES.items():
        out = "docs/licenses/OFL-%s.txt" % name
        open(out, "wb").write(fetch(path))
        print(out)
