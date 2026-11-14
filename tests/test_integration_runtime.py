"""Full-dependency smoke checks for the deployed application's Linux target."""

from pathlib import Path
import math
import struct
import wave

from PIL import Image
import pytest
from PyPDF2 import PdfReader, PdfWriter


def test_poppler_pdf_conversion(tmp_path):
    from File_Handling.convert_pdf_to_images import convert_pdf_to_images
    source = tmp_path / "source.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=150)
    with source.open("wb") as handle:
        writer.write(handle)
    images = convert_pdf_to_images(str(source))
    assert len(images) == 1
    assert isinstance(images[0], Image.Image)
    assert images[0].width > 0


def test_libreoffice_docx_conversion(tmp_path):
    from docx import Document
    from File_Handling.convert_word_doc_to_pdf import convert_word_doc_to_pdf
    source = tmp_path / "example.docx"
    destination = tmp_path / "example.pdf"
    document = Document()
    document.add_paragraph("Smoke test for Word-to-PDF.")
    document.save(source)
    convert_word_doc_to_pdf(str(source), str(destination))
    assert destination.is_file()
    assert len(PdfReader(str(destination)).pages) >= 1


def test_speech_file_output(tmp_path):
    from Audio_Speech_Processing.text_to_speech import text_to_speech
    destination = tmp_path / "speech.wav"
    text_to_speech("Testing speech generation.", output_path=str(destination))
    assert destination.is_file()
    assert destination.stat().st_size > 44


def test_pitch_analyser_returns_statistics(tmp_path):
    from Audio_Speech_Processing.analyse_pitch import analyse_pitch
    source = tmp_path / "tone.wav"
    sample_rate = 22050
    with wave.open(str(source), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        frames = (
            struct.pack("<h", int(10000 * math.sin(2 * math.pi * 220 * index / sample_rate)))
            for index in range(sample_rate)
        )
        output.writeframes(b"".join(frames))
    stats = analyse_pitch(str(source))
    assert 175 <= stats["median_Hz"] <= 270
    assert stats["duration_seconds"] == pytest.approx(1, abs=0.01)


def test_streamlit_all_navigation_pages():
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file("app.py", default_timeout=45).run()
    assert not app.exception
    pages = [
        "Audio & Speech Processing",
        "Automation & Productivity",
        "File Handling",
        "Git Utilities",
        "Hugging Face Utilities",
        "Image Processing",
        "Jupyter Notebook Utilities",
        "Regex Cheatsheet",
    ]
    for page in pages:
        app.sidebar.radio[0].set_value(page).run()
        assert not app.exception, page
