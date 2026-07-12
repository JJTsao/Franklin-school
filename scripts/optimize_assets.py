from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
BRAND_SOURCE = ROOT / "source-assets" / "brand"
OUTPUT = ROOT / "public" / "images" / "optimized" / "brand"


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


def optimize_brand_assets() -> None:
    with Image.open(BRAND_SOURCE / "logo-circle.png") as image:
        logo = image.convert("RGBA").resize((192, 192), Image.Resampling.LANCZOS)
        save_webp(logo, "logo-circle.webp", quality=90)

    with Image.open(BRAND_SOURCE / "mascot-point.png") as image:
        mascot = resize_to_width(image.convert("RGBA"), 380)
        save_webp(mascot, "mascot-point.webp", quality=88)


if __name__ == "__main__":
    optimize_brand_assets()
