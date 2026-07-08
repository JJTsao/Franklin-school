"""Regenerate the body-font subset from the full Noto Sans TC variable TTF.

Collects every printable character in index.html (plus ASCII and common CJK
punctuation) so any text styled with "Noto Sans TC Local" — nav, headings at
weight 900, ribbons, contact titles, body copy — renders without per-glyph
fallback to a system font. The wght axis (100-900) is preserved as a variable
font so both the light body weight and the 900 display weight keep working.

The previously shipped subset's characters are unioned in as a safety net so a
regeneration can never drop a glyph that some code path still renders.

Requires: pip install fonttools brotli
Usage:    python scripts/subset_noto_font.py
"""

from pathlib import Path
import string

from fontTools.subset import Options, Subsetter, load_font, save_font
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FONT = ROOT / "source-assets" / "fonts" / "NotoSansTC-VF.ttf"
PAGE = ROOT / "index.html"
OUTPUT = ROOT / "public" / "fonts" / "NotoSansTC-Subset.woff2"

EXTRA_CHARACTERS = "×→（）「」『』！？：；、。，・．–—…％／"


def collect_characters() -> str:
    content = PAGE.read_text(encoding="utf-8")
    characters = {char for char in content if char.isprintable() and not char.isspace()}
    characters.update(string.digits + string.ascii_letters + string.punctuation)
    characters.update(EXTRA_CHARACTERS)
    # Safety net: keep every glyph the currently shipped subset already covers.
    if OUTPUT.exists():
        characters.update(chr(cp) for cp in TTFont(OUTPUT).getBestCmap())
    return "".join(sorted(characters))


def subset_font(text: str) -> None:
    options = Options()
    options.flavor = "woff2"
    options.desubroutinize = True
    # Keep the weight axis so font-weight: 100 900 stays a variable font.
    options.retain_gids = False
    font = load_font(SOURCE_FONT, options)
    subsetter = Subsetter(options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    save_font(font, OUTPUT, options)


def verify_coverage(text: str) -> list[str]:
    cmap = TTFont(OUTPUT).getBestCmap()
    return [char for char in text if ord(char) not in cmap]


def main() -> None:
    text = collect_characters()
    subset_font(text)
    missing = verify_coverage(text)
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"{OUTPUT.name}: {len(text)} chars requested, {size_kb:.0f} KB")
    if missing:
        print(f"WARNING: {len(missing)} chars missing from source font: {''.join(missing)}")


if __name__ == "__main__":
    main()
