"""Merge PDFs in deterministic filename order, excluding an existing output."""

from pathlib import Path

from pypdf import PdfWriter


def merge_pdfs_in_folder(folder_path: str, output_path: str) -> None:
    destination = Path(output_path).resolve()
    folder = Path(folder_path)
    if not folder.is_dir():
        raise NotADirectoryError(folder)
    files = sorted(
        (
            path for path in folder.iterdir()
            if path.is_file()
            and path.suffix.lower() == ".pdf"
            and path.resolve() != destination
        ),
        key=lambda path: path.name.casefold(),
    )
    if not files:
        raise ValueError("No PDF files were supplied")
    writer = PdfWriter()
    try:
        for path in files:
            writer.append(str(path))
        with destination.open("wb") as output:
            writer.write(output)
    finally:
        writer.close()
