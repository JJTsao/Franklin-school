from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "public" / "images"
GENERATED = ROOT / "source-assets" / "archive" / "generated"
OUTPUT = SOURCE / "optimized"


def resize_to_width(image: Image.Image, width: int) -> Image.Image:
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def save_webp(image: Image.Image, name: str, *, quality: int = 82) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    image.save(
        OUTPUT / name,
        "WEBP",
        quality=quality,
        method=6,
        exact=True,
    )


def optimize_photos() -> None:
    with Image.open(GENERATED / "hero-classroom-v2.png") as image:
        save_webp(resize_to_width(image.convert("RGB"), 1440), "hero-classroom.webp", quality=82)

    program_settings = {
        "program-english-v2.png": ("program-english.webp", "program-english-mobile.webp", 40),
        "program-care-v2.png": ("program-care.webp", "program-care-mobile.webp", 170),
    }
    for source_name, (desktop_name, mobile_name, crop_top) in program_settings.items():
        with Image.open(GENERATED / source_name) as image:
            image = image.convert("RGB")
            save_webp(resize_to_width(image, 720), desktop_name, quality=82)
            square = image.crop((0, crop_top, image.width, crop_top + image.width))
            square = square.resize((720, 720), Image.Resampling.LANCZOS)
            save_webp(square, mobile_name, quality=84)

    gallery_names = [
        "gallery-achievement-v2.png",
        "gallery-story-v2.png",
        "gallery-presentation-v2.png",
        "gallery-science-v2.png",
        "gallery-teamwork-v2.png",
    ]
    for source_name in gallery_names:
        with Image.open(GENERATED / source_name) as image:
            image = image.convert("RGB").resize((640, 480), Image.Resampling.LANCZOS)
            save_webp(image, source_name.replace("-v2.png", ".webp"), quality=80)


def optimize_brand_assets() -> None:
    with Image.open(SOURCE / "logo-circle.png") as image:
        logo = image.convert("RGBA").resize((192, 192), Image.Resampling.LANCZOS)
        save_webp(logo, "logo-circle.webp", quality=90)

    with Image.open(SOURCE / "mascot-point.png") as image:
        mascot = resize_to_width(image.convert("RGBA"), 380)
        save_webp(mascot, "mascot-point.webp", quality=88)


if __name__ == "__main__":
    optimize_photos()
    optimize_brand_assets()
