from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "assets" / "classroom-originals"
OUTPUT = ROOT / "output" / "classroom-previews"
WEB_OUTPUT = ROOT / "public" / "images" / "optimized"


@dataclass(frozen=True)
class Preview:
    source: Path
    output_name: str
    size: tuple[int, int]
    crop_box: tuple[int, int, int, int] | None = None
    focus: tuple[float, float] = (0.5, 0.5)
    brightness: float = 1.0
    contrast: float = 1.0
    color: float = 1.0
    white_balance: tuple[float, float, float] = (1.0, 1.0, 1.0)


PREVIEWS = [
    Preview(
        SOURCE / "斗六斗南分校圖片" / "全部答對.JPG",
        "hero-全部答對-3x2.jpg",
        (1800, 1200),
        brightness=0.96,
        contrast=1.05,
        color=0.96,
        white_balance=(0.98, 1.0, 1.04),
    ),
    Preview(
        SOURCE / "上課照片" / "遊戲融入教學.JPG",
        "gallery-遊戲融入教學-4x3.jpg",
        (1600, 1200),
        focus=(0.52, 0.5),
        brightness=0.98,
        contrast=1.04,
        color=0.96,
        white_balance=(0.98, 1.0, 1.04),
    ),
    Preview(
        SOURCE / "上課照片" / "學習也可以充滿歡樂.JPG",
        "program-學習也可以充滿歡樂-4x5.jpg",
        (1200, 1500),
        # Anchor at the top to preserve the teacher's full head, trim the
        # distracting foreground workbook, and remove the partial person on
        # the far right while keeping the laughing students.
        crop_box=(80, 0, 1280, 1500),
        brightness=0.98,
        contrast=1.04,
        color=0.97,
        white_balance=(0.98, 1.0, 1.03),
    ),
    Preview(
        SOURCE / "斗六斗南分校圖片" / "勇於嘗試是芝蔴街美語的特色.JPG",
        "gallery-勇於嘗試-4x3.jpg",
        (1600, 1200),
        focus=(0.47, 0.5),
        brightness=0.97,
        contrast=1.04,
        color=0.97,
        white_balance=(0.98, 1.0, 1.03),
    ),
    Preview(
        SOURCE / "斗六斗南分校圖片" / "Who want to say it？.JPG",
        "gallery-主動舉手-4x3.jpg",
        (1600, 1200),
        # Keep the active students and first teacher while excluding the
        # right-hand whiteboard section that contains student names.
        crop_box=(0, 160, 3200, 2560),
        brightness=0.95,
        contrast=1.06,
        color=0.95,
        white_balance=(0.97, 1.0, 1.05),
    ),
]


WEB_ASSETS = [
    Preview(
        SOURCE / "斗六斗南分校圖片" / "全部答對.JPG",
        "classroom-hero.webp",
        (1440, 960),
        brightness=0.96,
        contrast=1.05,
        color=0.96,
        white_balance=(0.98, 1.0, 1.04),
    ),
    Preview(
        SOURCE / "上課照片" / "遊戲融入教學.JPG",
        "classroom-program-english.webp",
        (720, 900),
        crop_box=(100, 0, 1188, 1360),
        brightness=0.98,
        contrast=1.04,
        color=0.96,
        white_balance=(0.98, 1.0, 1.04),
    ),
    Preview(
        SOURCE / "上課照片" / "遊戲融入教學.JPG",
        "classroom-program-english-mobile.webp",
        (720, 720),
        crop_box=(0, 0, 1360, 1360),
        brightness=0.98,
        contrast=1.04,
        color=0.96,
        white_balance=(0.98, 1.0, 1.04),
    ),
    Preview(
        SOURCE / "上課照片" / "學習也可以充滿歡樂.JPG",
        "classroom-program-care.webp",
        (720, 900),
        crop_box=(80, 0, 1280, 1500),
        brightness=0.98,
        contrast=1.04,
        color=0.97,
        white_balance=(0.98, 1.0, 1.03),
    ),
    Preview(
        SOURCE / "上課照片" / "學習也可以充滿歡樂.JPG",
        "classroom-program-care-mobile.webp",
        (720, 720),
        crop_box=(0, 0, 1360, 1360),
        brightness=0.98,
        contrast=1.04,
        color=0.97,
        white_balance=(0.98, 1.0, 1.03),
    ),
    Preview(
        SOURCE / "斗六斗南分校圖片" / "勇於嘗試是芝蔴街美語的特色.JPG",
        "classroom-gallery-brave.webp",
        (640, 480),
        focus=(0.47, 0.5),
        brightness=0.97,
        contrast=1.04,
        color=0.97,
        white_balance=(0.98, 1.0, 1.03),
    ),
    Preview(
        SOURCE / "斗六斗南分校圖片" / "Who want to say it？.JPG",
        "classroom-gallery-hands-up.webp",
        (640, 480),
        crop_box=(0, 160, 3200, 2560),
        brightness=0.95,
        contrast=1.06,
        color=0.95,
        white_balance=(0.97, 1.0, 1.05),
    ),
    Preview(
        SOURCE / "斗六斗南分校圖片" / "Please try again.JPG",
        "classroom-gallery-encouragement.webp",
        (640, 480),
        focus=(0.72, 0.5),
        brightness=0.97,
        contrast=1.04,
        color=0.96,
        white_balance=(0.98, 1.0, 1.04),
    ),
    Preview(
        SOURCE / "上課照片" / "誰要來挑戰？.JPG",
        "classroom-gallery-challenge.webp",
        (640, 480),
        focus=(0.54, 0.5),
        brightness=0.98,
        contrast=1.04,
        color=0.96,
        white_balance=(0.98, 1.0, 1.04),
    ),
    Preview(
        SOURCE / "上課照片" / "教授【單字解釋】 小朋友學得比較辛苦.JPG",
        "classroom-gallery-english-context.webp",
        (640, 480),
        focus=(0.28, 0.5),
        brightness=0.99,
        contrast=1.03,
        color=0.97,
        white_balance=(0.99, 1.0, 1.02),
    ),
]


def crop_to_ratio(
    image: Image.Image,
    ratio: float,
    focus: tuple[float, float],
) -> Image.Image:
    width, height = image.size
    current = width / height
    if abs(current - ratio) < 0.001:
        return image

    focus_x = min(max(focus[0], 0.0), 1.0)
    focus_y = min(max(focus[1], 0.0), 1.0)
    if current > ratio:
        crop_width = round(height * ratio)
        left = round((width - crop_width) * focus_x)
        left = min(max(left, 0), width - crop_width)
        return image.crop((left, 0, left + crop_width, height))

    crop_height = round(width / ratio)
    top = round((height - crop_height) * focus_y)
    top = min(max(top, 0), height - crop_height)
    return image.crop((0, top, width, top + crop_height))


def balance_channels(
    image: Image.Image,
    multipliers: tuple[float, float, float],
) -> Image.Image:
    channels = image.split()
    adjusted = []
    for channel, multiplier in zip(channels, multipliers, strict=True):
        adjusted.append(channel.point(lambda value, m=multiplier: min(255, round(value * m))))
    return Image.merge("RGB", adjusted)


def create_asset(spec: Preview, output_dir: Path) -> Path:
    with Image.open(spec.source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")

    if spec.crop_box is not None:
        image = image.crop(spec.crop_box)
    image = crop_to_ratio(image, spec.size[0] / spec.size[1], spec.focus)
    image = balance_channels(image, spec.white_balance)
    image = ImageEnhance.Brightness(image).enhance(spec.brightness)
    image = ImageEnhance.Contrast(image).enhance(spec.contrast)
    image = ImageEnhance.Color(image).enhance(spec.color)
    image = image.resize(spec.size, Image.Resampling.LANCZOS)
    image = ImageEnhance.Sharpness(image).enhance(1.06)

    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / spec.output_name
    if destination.suffix.lower() == ".webp":
        image.save(destination, "WEBP", quality=82, method=6)
    else:
        image.save(destination, "JPEG", quality=91, optimize=True, progressive=True)
    return destination


def create_preview(spec: Preview) -> Path:
    return create_asset(spec, OUTPUT)


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in (
        Path(r"C:\Windows\Fonts\msjh.ttc"),
        Path(r"C:\Windows\Fonts\mingliu.ttc"),
    ):
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def create_contact_sheet(paths: list[Path]) -> Path:
    tile_size = (640, 480)
    label_height = 58
    margin = 24
    columns = 2
    rows = 3
    sheet = Image.new(
        "RGB",
        (
            margin + columns * (tile_size[0] + margin),
            margin + rows * (tile_size[1] + label_height + margin),
        ),
        "#f5f2e9",
    )
    draw = ImageDraw.Draw(sheet)
    font = load_font(24)

    for index, path in enumerate(paths):
        row, column = divmod(index, columns)
        x = margin + column * (tile_size[0] + margin)
        y = margin + row * (tile_size[1] + label_height + margin)
        with Image.open(path) as opened:
            tile = ImageOps.contain(opened.convert("RGB"), tile_size, Image.Resampling.LANCZOS)
        tile_x = x + (tile_size[0] - tile.width) // 2
        tile_y = y + (tile_size[1] - tile.height) // 2
        sheet.paste(tile, (tile_x, tile_y))
        label = path.stem.replace("gallery-", "").replace("program-", "").replace("hero-", "")
        draw.text((x + 8, y + tile_size[1] + 10), label, fill="#173c2b", font=font)

    destination = OUTPUT / "前五張校正預覽-聯絡表.jpg"
    sheet.save(destination, "JPEG", quality=90, optimize=True, progressive=True)
    return destination


if __name__ == "__main__":
    generated = [create_preview(spec) for spec in PREVIEWS]
    generated.append(create_contact_sheet(generated))
    generated.extend(create_asset(spec, WEB_OUTPUT) for spec in WEB_ASSETS)
    for path in generated:
        print(path.relative_to(ROOT))
