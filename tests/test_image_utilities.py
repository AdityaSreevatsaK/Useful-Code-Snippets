from PIL import Image

from Image_Processing.compress_image_by_percentage import compress_image_by_percentage
from Image_Processing.convert_image_format import convert_image_format


def test_full_compression_never_creates_zero_dimensions():
    image = Image.new("RGBA", (1, 1), (255, 0, 0, 0))
    result = compress_image_by_percentage(image, 100)
    assert result.size == (1, 1)


def test_png_format_retains_transparency(tmp_path):
    source = tmp_path / "original.png"
    target = tmp_path / "converted.png"
    Image.new("RGBA", (4, 4), (1, 2, 3, 0)).save(source)
    convert_image_format(str(source), str(target), "PNG")
    with Image.open(target) as output:
        assert output.convert("RGBA").getpixel((0, 0))[3] == 0


def test_jpeg_replaces_alpha_with_white(tmp_path):
    source = tmp_path / "original.png"
    target = tmp_path / "converted.jpeg"
    Image.new("RGBA", (4, 4), (1, 2, 3, 0)).save(source)
    convert_image_format(str(source), str(target), "JPEG")
    with Image.open(target) as output:
        assert output.mode == "RGB"
