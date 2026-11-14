"""Resize local images safely, preserving file formats."""

from pathlib import Path

from PIL import Image


def resize_all_images_in_folder(folder_path: str, percentage: float) -> list[str]:
    if not 0 < percentage <= 100:
        raise ValueError("Resize percentage must be between 0 and 100")
    updated = []
    for path in Path(folder_path).iterdir():
        if path.suffix.lower() not in (".png", ".jpg", ".jpeg") or not path.is_file():
            continue
        with Image.open(path) as original:
            size = (max(1, round(original.width * percentage / 100)),
                    max(1, round(original.height * percentage / 100)))
            resized = original.resize(size, Image.Resampling.LANCZOS)
            resized.save(path, format=original.format)
        updated.append(str(path))
    return updated
