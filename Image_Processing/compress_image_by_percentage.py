"""Reduce image dimensions by a user-specified percentage."""

from PIL import Image


def compress_image_by_percentage(image: Image.Image, percentage_to_compress: int) -> Image.Image:
    if not 0 <= percentage_to_compress <= 100:
        raise ValueError("Compression percentage must be between 0 and 100")
    remaining = (100 - percentage_to_compress) / 100
    width = max(1, round(image.width * remaining))
    height = max(1, round(image.height * remaining))
    return image.resize((width, height), Image.Resampling.LANCZOS)
