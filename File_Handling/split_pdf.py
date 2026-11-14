"""Split a PDF into one file per page."""

from pathlib import Path
from pypdf import PdfReader, PdfWriter


def split_pdf(input_path: str, output_folder: str) -> list[str]:
    folder = Path(output_folder)
    folder.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(input_path)
    outputs = []
    for index, page in enumerate(reader.pages, 1):
        writer = PdfWriter()
        writer.add_page(page)
        destination = folder / f"page_{index}.pdf"
        with destination.open("wb") as handle:
            writer.write(handle)
        outputs.append(str(destination))
    return outputs
