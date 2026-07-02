from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "public/images/optimized/classroom-hero.webp"
OUTPUT = SOURCE.parent


def save_crop(filename: str, box: tuple[int, int, int, int], size=None) -> None:
    with Image.open(SOURCE) as source:
        crop = source.convert("RGB").crop(box)
        if size is not None:
            crop = crop.resize(size, Image.Resampling.LANCZOS)
        crop.save(OUTPUT / filename, "WEBP", quality=86, method=6)


# Keep the full horizontal classroom action while removing excess whiteboard.
save_crop("classroom-hero-desktop.webp", (0, 150, 1440, 960))
save_crop("classroom-hero-tablet.webp", (0, 96, 1440, 960))
save_crop("classroom-hero-mobile.webp", (0, 150, 1440, 960), (1280, 720))
