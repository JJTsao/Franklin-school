from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source-assets" / "teachers" / "current-teachers.jpg"
TEACHER_SOURCE = ROOT / "source-assets" / "teachers"
OUTPUT = ROOT / "public" / "images" / "optimized" / "teachers"

# 新版師資合照中四張既有肖像的裁切框（皆為 4:5）。Jenny 稍微收緊左右，
# 消除舊照造成的偏寬視覺，同時保留自然的頭肩比例。
CROPS = {
    "amber-chen": (33, 20, 313, 370),
    "gloria-hu": (372, 22, 646, 365),
    "heather-huntley": (685, 22, 959, 365),
    "jenny-lin": (47, 507, 301, 825),
}


def save_teacher(name: str, photo: Image.Image) -> None:
    source_path = TEACHER_SOURCE / f"{name}.jpg"
    output_path = OUTPUT / f"{name}.webp"

    photo.save(source_path, "JPEG", quality=95, optimize=True)
    web_photo = photo.resize((608, 760), Image.Resampling.LANCZOS)
    web_photo.save(output_path, "WEBP", quality=84, method=6)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE) as source:
        image = source.convert("RGB")
        for name, box in CROPS.items():
            save_teacher(name, image.crop(box))


if __name__ == "__main__":
    main()
