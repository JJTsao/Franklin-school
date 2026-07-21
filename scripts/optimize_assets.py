from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
BRAND_SOURCE = ROOT / "source-assets" / "brand"
BRANCH_SOURCE = ROOT / "source-assets" / "branch"
TEACHER_SOURCE = ROOT / "source-assets" / "teachers"
OUTPUT = ROOT / "public" / "images" / "optimized" / "brand"
BRANCH_OUTPUT = ROOT / "public" / "images" / "optimized" / "branch"
TEACHER_OUTPUT = ROOT / "public" / "images" / "optimized" / "teachers"


def resize_to_width(image: Image.Image, width: int) -> Image.Image:
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def crop_to_ratio(image: Image.Image, ratio_w: int, ratio_h: int) -> Image.Image:
    target = ratio_w / ratio_h
    current = image.width / image.height
    if current > target:
        new_width = round(image.height * target)
        left = (image.width - new_width) // 2
        return image.crop((left, 0, left + new_width, image.height))
    new_height = round(image.width / target)
    top = (image.height - new_height) // 2
    return image.crop((0, top, image.width, top + new_height))


def save_webp(image: Image.Image, name: str, *, quality: int = 82, output: Path = OUTPUT) -> None:
    output.mkdir(parents=True, exist_ok=True)
    image.save(
        output / name,
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


def optimize_branch_assets() -> None:
    # 分校門面照：裁成 3:4 直式，輸出首屏所需的 400px 與 720px 響應式版本。
    # 400px 足以覆蓋手機雙欄與平板側欄；720px 保留高密度桌機螢幕的清晰度。
    sources = {
        "branch-douliu.jpg": "branch-douliu",
        "branch-dounan-neighbor-blur-v2.png": "branch-dounan",
    }
    for src_name, output_stem in sources.items():
        with Image.open(BRANCH_SOURCE / src_name) as image:
            photo = crop_to_ratio(image.convert("RGB"), 3, 4)
            save_webp(
                resize_to_width(photo, 400),
                f"{output_stem}-400.webp",
                quality=62,
                output=BRANCH_OUTPUT,
            )
            save_webp(
                resize_to_width(photo, 720),
                f"{output_stem}.webp",
                quality=62,
                output=BRANCH_OUTPUT,
            )


def optimize_teacher_assets() -> None:
    # 師資大頭照：裁成 4:5 直式（對齊師資卡片 .photo-frame）。
    for source in sorted(TEACHER_SOURCE.glob("*.jpg")):
        with Image.open(source) as image:
            photo = crop_to_ratio(image.convert("RGB"), 4, 5)
            save_webp(photo, f"{source.stem}.webp", quality=84, output=TEACHER_OUTPUT)


if __name__ == "__main__":
    optimize_brand_assets()
    optimize_branch_assets()
    optimize_teacher_assets()
