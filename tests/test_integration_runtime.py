"""Full-dependency smoke checks for the deployed application's Linux target."""

import math
import struct
import wave

from pathlib import Path

from PIL import Image
import pytest
import cv2

from Image_Processing.convert_and_display_grayscale import convert_and_display
from Image_Processing.resize_all_images_in_folder import resize_all_images_in_folder
from pypdf import PdfReader, PdfWriter


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
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py", default_timeout=45).run()
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


"""Smoke-check public Streamlit controls on the configured hosted runtime."""

def test_privileged_controls_are_disabled_on_public_dashboard(monkeypatch):
    monkeypatch.delenv("ENABLE_LOCAL_OPERATIONS", raising=False)
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py", default_timeout=45).run()
    assert not app.exception
    protected = {
        "Automation & Productivity": ("Check Status", "Run Logging Setup"),
        "File Handling": ("Check Disk Usage", "Find Largest File", "Generate Tree"),
        "Git Utilities": ("Check Git Status", "Get Repos"),
        "Hugging Face Utilities": ("Delete Folder",),
    }
    for section, labels in protected.items():
        app.sidebar.radio[0].set_value(section).run()
        assert not app.exception, section
        for label in labels:
            buttons = [button for button in app.button if button.label == label]
            assert len(buttons) == 1, (section, label)
            assert buttons[0].disabled, (section, label)



def test_greyscale_conversion_returns_pixels_without_gui(tmp_path):
    source = tmp_path / "original.png"
    output = tmp_path / "greyscale.png"
    Image.new("RGB", (6, 4), (240, 60, 30)).save(source)
    pixels = convert_and_display(str(source), str(output))
    assert pixels.shape == (4, 6)
    assert output.is_file()
    saved = cv2.imread(str(output), cv2.IMREAD_GRAYSCALE)
    assert saved.shape == pixels.shape


def test_bulk_resize_never_creates_zero_dimensions(tmp_path):
    path = tmp_path / "tiny.png"
    Image.new("RGB", (1, 1)).save(path)
    result = resize_all_images_in_folder(str(tmp_path), 1)
    assert str(path) in result
    with Image.open(path) as image:
        assert image.size == (1, 1)
