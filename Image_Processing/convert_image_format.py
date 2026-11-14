"""Convert images without silently discarding alpha in PNG or GIF output."""

from pathlib import Path
from shutil import copyfile

from PIL import Image


def convert_image_format(input_path: str, output_path: str, image_format: str = "JPEG") -> None:
    fmt = image_format.upper()
    if fmt not in ("JPEG", "PNG", "GIF"):
        raise ValueError("Unsupported output format")
    # Re-encoding an animated GIF as a single frame would destroy animation.
    if fmt == "GIF":
        with Image.open(input_path) as source:
            if getattr(source, "is_animated", False):
                if Path(input_path).resolve() != Path(output_path).resolve():
                    copyfile(input_path, output_path)
                return
    with Image.open(input_path) as original:
        image = original.copy()
    if fmt == "JPEG":
        if image.mode in ("RGBA", "LA") or "transparency" in image.info:
            rgba = image.convert("RGBA")
            background = Image.new("RGB", rgba.size, "white")
            background.paste(rgba, mask=rgba.getchannel("A"))
            image = background
        else:
            image = image.convert("RGB")
    elif fmt == "GIF":
        image = image.convert("RGBA").quantize(colors=255)
    image.save(output_path, format=fmt)
