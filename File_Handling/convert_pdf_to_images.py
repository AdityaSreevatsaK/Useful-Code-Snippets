"""Convert a PDF to images in memory, without writing to the server cwd."""

from pdf2image import convert_from_path


def convert_pdf_to_images(pdf_path: str, dpi: int = 120):
    """Return one Pillow image per page. Requires Poppler on PATH."""
    if dpi < 30 or dpi > 300:
        raise ValueError("DPI must be between 30 and 300")
    return convert_from_path(pdf_path, dpi=dpi, fmt="png")
