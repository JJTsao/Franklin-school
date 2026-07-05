"""Color-grade the real classroom photos into the brand's warm palette.

Grades every top-of-chain classroom webp: warms the fluorescent white balance,
lifts midtones, and selectively desaturates the saturated red plastic chairs
that clash with the green/yellow brand palette. Derived hero crops are
regenerated afterwards via create_hero_crops.py.

Idempotent: on first run the pristine sources are copied to
source-assets/classroom-pregrade/; later runs always grade from those copies,
so tweaking the recipe never double-grades. The camera originals are not in
the repo — if they become available, re-run create_classroom_previews.py
first, delete the pregrade folder, then run this script again.

Requires: pip install pillow
Usage:    python scripts/grade_classroom_photos.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OPTIMIZED = ROOT / "public" / "images" / "optimized"
PREGRADE = ROOT / "source-assets" / "classroom-pregrade"

FILES = [
    "classroom-hero.webp",
    "classroom-program-english.webp",
    "classroom-program-english-mobile.webp",
    "classroom-program-care.webp",
    "classroom-program-care-mobile.webp",
    "classroom-gallery-brave.webp",
    "classroom-gallery-hands-up.webp",
    "classroom-gallery-challenge.webp",
    "classroom-gallery-encouragement.webp",
    "classroom-gallery-english-context.webp",
]

WHITE_BALANCE = (1.045, 1.005, 0.94)
BRIGHTNESS = 1.06
CONTRAST = 1.03
SATURATION = 1.02
RED_DESATURATION = 0.55

# PIL hue runs 0-255 (red wraps around 0); ramps keep skin tones out of the mask.
HUE_FULL, HUE_ZERO = 10, 20
SAT_ZERO, SAT_FULL = 100, 140


def hue_weight(hue: int) -> int:
    distance = min(hue, 256 - hue)
    if distance <= HUE_FULL:
        return 255
    if distance >= HUE_ZERO:
        return 0
    return round(255 * (HUE_ZERO - distance) / (HUE_ZERO - HUE_FULL))


def sat_weight(saturation: int) -> int:
    if saturation <= SAT_ZERO:
        return 0
    if saturation >= SAT_FULL:
        return 255
    return round(255 * (saturation - SAT_ZERO) / (SAT_FULL - SAT_ZERO))


def desaturate_reds(image: Image.Image) -> Image.Image:
    hue, saturation, value = image.convert("HSV").split()
    mask = ImageChops.multiply(hue.point(hue_weight), saturation.point(sat_weight))
    mask = mask.filter(ImageFilter.GaussianBlur(3))
    muted = saturation.point(lambda s: round(s * RED_DESATURATION))
    saturation = Image.composite(muted, saturation, mask)
    return Image.merge("HSV", (hue, saturation, value)).convert("RGB")


def balance_channels(image: Image.Image, multipliers: tuple[float, float, float]) -> Image.Image:
    channels = [
        channel.point(lambda v, m=m: min(255, round(v * m)))
        for channel, m in zip(image.split(), multipliers)
    ]
    return Image.merge("RGB", channels)


def grade(image: Image.Image) -> Image.Image:
    image = desaturate_reds(image.convert("RGB"))
    image = balance_channels(image, WHITE_BALANCE)
    image = ImageEnhance.Brightness(image).enhance(BRIGHTNESS)
    image = ImageEnhance.Contrast(image).enhance(CONTRAST)
    image = ImageEnhance.Color(image).enhance(SATURATION)
    return image


def main() -> None:
    PREGRADE.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        pristine = PREGRADE / name
        if not pristine.exists():
            shutil.copy2(OPTIMIZED / name, pristine)
        with Image.open(pristine) as source:
            graded = grade(source)
        graded.save(OPTIMIZED / name, "WEBP", quality=88, method=6)
        print(f"graded {name}")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "create_hero_crops.py")], check=True)
    print("regenerated hero crops")


if __name__ == "__main__":
    main()
