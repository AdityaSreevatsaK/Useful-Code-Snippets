"""Convert DOCX to PDF on Windows/macOS or Linux with LibreOffice."""

from pathlib import Path
import shutil
import subprocess
import sys


def convert_word_doc_to_pdf(word_folder_path: str, pdf_folder_path: str | None = None) -> None:
    source = Path(word_folder_path)
    destination = Path(pdf_folder_path) if pdf_folder_path else source.with_suffix(".pdf")
    destination.parent.mkdir(parents=True, exist_ok=True)

    if sys.platform in ("win32", "darwin"):
        from docx2pdf import convert
        convert(str(source), str(destination))
        return

    binary = shutil.which("libreoffice") or shutil.which("soffice")
    if not binary:
        raise RuntimeError("DOCX to PDF on Linux requires LibreOffice")
    result = subprocess.run(
        [binary, "--headless", "--convert-to", "pdf", "--outdir",
         str(destination.parent), str(source)],
        capture_output=True, text=True, check=False, timeout=120,
    )
    generated = destination.parent / (source.stem + ".pdf")
    if result.returncode != 0 or not generated.exists():
        raise RuntimeError("LibreOffice conversion failed: " + result.stderr[-500:])
    if generated.resolve() != destination.resolve():
        generated.replace(destination)
