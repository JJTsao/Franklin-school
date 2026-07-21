from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source-assets/classroom/current-hero.jpg"
OUTPUT = ROOT / "public/images/optimized/classroom"


def save_crop(filename: str, box: tuple[int, int, int, int], size=None) -> None:
    with Image.open(SOURCE) as source:
        crop = ImageOps.exif_transpose(source).convert("RGB").crop(box)
        if size is not None:
            crop = crop.resize(size, Image.Resampling.LANCZOS)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        crop.save(OUTPUT / filename, "WEBP", quality=84, method=6)


# Retain a 3:2 source frame, anchored to the teacher on the left. Trimming
# only the excess room on the right keeps the class interaction as the focus.
with Image.open(SOURCE) as image:
    source = ImageOps.exif_transpose(image).convert("RGB")
    crop_width = round(source.width * 0.9)
    crop_height = round(crop_width / 1.5)
    crop_top = (source.height - crop_height) // 2
    crop_box = (0, crop_top, crop_width, crop_top + crop_height)

save_crop("classroom-hero.webp", crop_box, (1440, 960))
save_crop("classroom-hero-desktop.webp", crop_box, (1440, 960))
save_crop("classroom-hero-tablet.webp", crop_box, (1440, 960))
save_crop("classroom-hero-mobile.webp", crop_box, (1152, 768))
save_crop("classroom-hero-mobile-800.webp", crop_box, (800, 533))
