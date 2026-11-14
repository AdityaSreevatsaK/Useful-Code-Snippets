"""Convert a PDF document into DOCX."""

from pdf2docx import Converter


def convert_pdf_to_word(pdf_file_path: str, word_file_path: str) -> None:
    converter = Converter(pdf_file_path)
    try:
        converter.convert(word_file_path, start=0, end=None)
    finally:
        converter.close()
