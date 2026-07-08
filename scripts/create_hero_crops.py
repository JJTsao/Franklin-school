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


# Keep the full-width original frame. The hero container is narrower than 16:9,
# so pre-cropping to 16:9 causes object-fit to cut into the teacher a second time.
save_crop("classroom-hero-desktop.webp", (0, 0, 1440, 960))
save_crop("classroom-hero-tablet.webp", (0, 0, 1440, 960))
save_crop("classroom-hero-mobile.webp", (0, 0, 1440, 960), (1152, 768))
