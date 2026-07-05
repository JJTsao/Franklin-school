"""Regenerate the display-font subset from the full jf-openhuninn TTF.

Collects every printable character that appears in index.html (plus ASCII and
common CJK punctuation) so any text styled with the display font — hero title,
section headings, ribbons, CTA highlight — renders without fallback mixing.

Requires: pip install fonttools brotli
Usage:    python scripts/subset_display_font.py
"""

from pathlib import Path
import string

from fontTools.subset import Options, Subsetter, load_font, save_font
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FONT = ROOT / "source-assets" / "fonts" / "jf-openhuninn-2.1.ttf"
PAGE = ROOT / "index.html"
OUTPUT = ROOT / "public" / "fonts" / "JFOpenHuninn-Display-Subset.woff2"

EXTRA_CHARACTERS = "×→（）「」『』！？：；、。，・．–—…％／"


def collect_characters() -> str:
    content = PAGE.read_text(encoding="utf-8")
    characters = {char for char in content if char.isprintable() and not char.isspace()}
    characters.update(string.digits + string.ascii_letters + string.punctuation)
    characters.update(EXTRA_CHARACTERS)
    return "".join(sorted(characters))


def subset_font(text: str) -> None:
    options = Options()
    options.flavor = "woff2"
    options.desubroutinize = True
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
