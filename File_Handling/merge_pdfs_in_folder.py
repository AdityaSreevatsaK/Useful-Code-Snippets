"""Merge PDFs from a folder in filename order."""

from pathlib import Path

from PyPDF2 import PdfMerger


def merge_pdfs_in_folder(folder_path: str, output_path: str) -> None:
    """Do not accidentally merge an existing output document into itself."""
    destination = Path(output_path).resolve()
    files = sorted(
        (p for p in Path(folder_path).iterdir()
         if p.is_file() and p.suffix.lower() == ".pdf" and p.resolve() != destination),
        key=lambda p: p.name,
    )
    if not files:
        raise ValueError("No PDF files were supplied")
    merger = PdfMerger()
    try:
        for pdf in files:
            merger.append(str(pdf))
        merger.write(str(destination))
    finally:
        merger.close()
