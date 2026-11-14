"""Request-level tests for Utility Shelf's same-origin HTTP API and UI."""

import io
import zipfile

from fastapi.testclient import TestClient
from PIL import Image
from pypdf import PdfWriter

from server import MAX_FILE, app

client = TestClient(app)


def test_home_spa_and_assets():
    assert client.get("/").status_code == 200
    assert 'id="app"' in client.get("/").text
    assert client.get("/tools/pdf-to-word").status_code == 200
    assert client.get("/assets/styles.css").status_code == 200
    assert client.get("/assets/app.js").status_code == 200
    assert client.get("/assets/favicon.svg").status_code == 200
    assert client.get("/api/private").status_code == 404


def test_theme_contrast_and_keyboard_search():
    css = client.get("/assets/styles.css").text
    js = client.get("/assets/app.js").text
    for token in ("--input:#ffffff", "--input:#1a2840", "--ink-strong:#f5f8ff"):
        assert token in css
    assert 'data-theme="dark"' in css
    assert "event.ctrlKey" in js
    assert "URL.createObjectURL" in js
    assert 'aria-label="Search tools"' in js


def test_health_and_headers():
    response = client.get("/api/health")
    assert response.json()["status"] == "ok"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert "frame-ancestors" in response.headers["content-security-policy"]
    assert response.headers["cache-control"] == "no-store"


def test_catalogue_and_source_whitelist():
    result = client.get("/api/tools")
    assert result.status_code == 200
    data = result.json()
    assert len(data["tools"]) == 34
    assert len(data["categories"]) == 8
    assert len({tool["slug"] for tool in data["tools"]}) == 34
    assert client.get("/api/tools/upper-case/source").status_code == 200
    assert client.get("/api/tools/unknown/source").status_code == 404


def test_privileged_tools_are_blocked_even_if_local_flag_set(monkeypatch):
    monkeypatch.setenv("ENABLE_LOCAL_OPERATIONS", "1")
    for slug in ("hf-delete-folder", "github-repos", "file-tree", "website-status"):
        response = client.post("/api/tools/" + slug + "/run", data={"text": "hello"})
        assert response.status_code == 403, slug


def test_text_tools_and_email_validation():
    result = client.post("/api/tools/upper-case/run", data={"text": "Hello world"})
    assert result.status_code == 200
    assert result.json()["result"] == "HELLO WORLD"
    assert client.post("/api/tools/validate-email/run", data={"text": "x@example.com"}).json()["result"] is True
    assert client.post("/api/tools/validate-email/run", data={"text": "x@example..com"}).json()["result"] is False
    assert client.post("/api/tools/extract-dates/run", data={"text": "21/11/2026"}).json()["result"] == ["21/11/2026"]


def test_youtube_id_input_restrictions():
    assert client.post("/api/tools/embed-youtube/run", data={"text": "bad"}).status_code == 422
    assert client.post("/api/tools/embed-youtube/run", data={"text": "g91kQyy4G7E"}).json() == {
        "kind": "video", "result": "g91kQyy4G7E"
    }


def test_same_origin_and_invalid_options():
    bad = client.post("/api/tools/upper-case/run", data={"text": "hi"},
                      headers={"Origin": "https://malicious.example"})
    assert bad.status_code == 403
    assert client.post("/api/tools/upper-case/run", data={"text": "hi", "options": "invalid"}).status_code == 422
    assert client.post("/api/tools/invalid/run", data={"text": "hi"}).status_code == 404


def _image():
    b = io.BytesIO()
    Image.new("RGB", (10, 6), (40, 90, 160)).save(b, "PNG")
    return b.getvalue()


def _pdf():
    b = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=90, height=130)
    writer.write(b)
    return b.getvalue()


def test_image_greyscale_download():
    result = client.post("/api/tools/grayscale-image/run",
                         files=[("files", ("input.png", _image(), "image/png"))])
    assert result.status_code == 200, result.text
    assert result.headers["x-utility-filename"] == "greyscale.png"
    with Image.open(io.BytesIO(result.content)) as output:
        assert output.size == (10, 6)
        assert output.mode in {"L", "P"}


def test_pdf_split_download():
    result = client.post("/api/tools/split-pdf/run",
                         files=[("files", ("input.pdf", _pdf(), "application/pdf"))])
    assert result.status_code == 200, result.text
    with zipfile.ZipFile(io.BytesIO(result.content)) as output:
        assert output.namelist() == ["page_1.pdf"]


def test_archive_traversal_is_rejected():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zipped:
        zipped.writestr("../escape.txt", "bad")
    result = client.post("/api/tools/extract-zip/run",
                         files=[("files", ("bad.zip", buf.getvalue(), "application/zip"))])
    assert result.status_code == 422


def test_input_validation_and_size_limits():
    assert client.post("/api/tools/pdf-to-images/run").status_code == 422
    invalid = client.post("/api/tools/pdf-to-word/run",
                          files=[("files", ("invalid.txt", b"hello", "text/plain"))])
    assert invalid.status_code == 422
    huge = client.post("/api/tools/create-zip/run",
                       files=[("files", ("huge.bin", b"x" * (MAX_FILE + 1), "application/octet-stream"))])
    assert huge.status_code == 413


def test_read_only_git_reference():
    response = client.post("/api/tools/git-commands/run")
    assert response.status_code == 200
    assert response.json()["kind"] == "text"
