"""Utility Shelf API.

The public API exposes only approved, stateless conversions and text tools.
Privileged local utilities remain visible in the catalogue but cannot be run
over HTTP, even if ENABLE_LOCAL_OPERATIONS has been configured.
"""

from __future__ import annotations

import asyncio
import io
import json
import logging
import re
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader
from starlette.concurrency import run_in_threadpool

from dashboard_catalogue import CATEGORIES, TOOLS, TOOL_BY_SLUG

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "web"
MAX_FILE = 20 * 1024 * 1024
MAX_TOTAL = 40 * 1024 * 1024
MAX_FILES = 30
MAX_PIXELS = 25_000_000
MAX_PDF_PAGES = 50
Image.MAX_IMAGE_PIXELS = MAX_PIXELS
logger = logging.getLogger("utility_shelf")
MAX_CONCURRENT_OPERATIONS = 2
PROCESS_SLOTS = asyncio.Semaphore(MAX_CONCURRENT_OPERATIONS)

app = FastAPI(
    title="Utility Shelf API",
    version="3.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        origin = request.headers.get("origin")
        if origin and urlparse(origin).netloc.lower() != request.url.netloc.lower():
            return JSONResponse({"detail": "Cross-origin requests are not permitted"}, status_code=403)
    if request.url.path.startswith("/api/") and request.headers.get("content-length"):
        try:
            if int(request.headers["content-length"]) > MAX_TOTAL + 128 * 1024:
                return JSONResponse({"detail": "Request exceeds the 40 MiB limit"}, status_code=413)
        except ValueError:
            return JSONResponse({"detail": "Invalid request length"}, status_code=400)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self' data: blob:; font-src 'self'; media-src 'self' blob:; "
        "connect-src 'self'; frame-src https://www.youtube-nocookie.com; "
        "object-src 'none'; base-uri 'self'; frame-ancestors 'self' https://huggingface.co"
    )
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "utility-shelf"}


@app.get("/api/tools")
def tools():
    return {
        "categories": CATEGORIES,
        "tools": [
            {
                "slug": tool.slug, "category": tool.category,
                "title": tool.title, "icon": tool.icon,
                "description": tool.description, "source": tool.source,
                "tags": tool.tags.split(), "local_only": tool.local_only,
            }
            for tool in TOOLS
        ],
    }


@app.get("/api/tools/{slug}/source")
def source(slug: str):
    tool = TOOL_BY_SLUG.get(slug)
    if tool is None:
        raise HTTPException(404, "Unknown tool")
    source_path = ROOT / tool.source
    if not source_path.is_file():
        raise HTTPException(404, "Source unavailable")
    return Response(source_path.read_text(encoding="utf-8"), media_type="text/plain; charset=utf-8")


def _check_files(slug: str, items: list[tuple[str, bytes]]) -> None:
    required = {
        "pdf-to-word": {".pdf"}, "pdf-to-images": {".pdf"},
        "word-to-pdf": {".docx"}, "merge-pdfs": {".pdf"},
        "split-pdf": {".pdf"}, "create-zip": None,
        "extract-zip": {".zip"}, "recursive-unzip": {".zip"},
        "grayscale-image": {".png", ".jpg", ".jpeg", ".gif", ".webp"},
        "compress-image": {".png", ".jpg", ".jpeg", ".gif", ".webp"},
        "convert-image": {".png", ".jpg", ".jpeg", ".gif", ".webp"},
        "resize-images": {".png", ".jpg", ".jpeg", ".gif", ".webp"},
        "pitch-analysis": {".wav", ".mp3", ".flac", ".ogg"},
        "notebook-to-python": {".ipynb"},
    }
    allowed = required.get(slug, ())
    if slug in required and not items:
        raise HTTPException(422, "Select a file to continue")
    if slug not in {"create-zip", "merge-pdfs", "resize-images"} and len(items) > 1:
        raise HTTPException(422, "This tool accepts one file")
    for name, data in items:
        if allowed is not None and Path(name).suffix.lower() not in allowed:
            raise HTTPException(422, "Unsupported file format")
        if Path(name).suffix.lower() == ".pdf" and not data.lstrip().startswith(b"%PDF-"):
            raise HTTPException(422, "Invalid PDF header")
    if len(items) > MAX_FILES:
        raise HTTPException(413, "Too many uploaded files")


def _options(raw: str) -> dict:
    try:
        result = json.loads(raw)
    except (json.JSONDecodeError, TypeError) as exc:
        raise HTTPException(422, "Invalid options") from exc
    if not isinstance(result, dict):
        raise HTTPException(422, "Options must be an object")
    return result


def _number(options: dict, name: str, default: int, low: int, high: int) -> int:
    value = options.get(name, default)
    if type(value) is not int or not low <= value <= high:
        raise HTTPException(422, f"{name} must be between {low} and {high}")
    return value


def _file(data: bytes, name: str, mime: str):
    return ("file", data, name, mime)


def _text(value):
    return ("json", {"kind": "text", "result": value})


def _pdf_pages(path: Path) -> int:
    pages = len(PdfReader(str(path)).pages)
    if not 1 <= pages <= MAX_PDF_PAGES:
        raise HTTPException(422, f"PDF must contain 1 to {MAX_PDF_PAGES} pages")
    return pages


def _make_zip(paths: list[Path], base: Path) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            if path.is_file():
                archive.write(path, path.relative_to(base).as_posix())
    return output.getvalue()


def _execute(slug: str, items: list[tuple[str, bytes]], text: str, opts: dict):
    """Perform an approved operation in an isolated temporary directory."""
    with tempfile.TemporaryDirectory(prefix="utility-shelf-") as temp:
        root = Path(temp)
        if slug in {
            "upper-case", "lower-case", "sentence-case", "extract-dates",
            "extract-hashtags", "extract-urls", "find-phone-numbers",
            "validate-email", "remove-spaces",
        }:
            if len(text) > 100_000:
                raise HTTPException(413, "Text exceeds 100,000 characters")
            from Regex_Cheatsheet.convert_text_to_upper_case import to_upper_case
            from Regex_Cheatsheet.convert_text_to_lower_case import to_lower_case
            from Regex_Cheatsheet.convert_text_to_sentence_case import to_sentence_case
            from Regex_Cheatsheet.extract_dates import extract_dates
            from Regex_Cheatsheet.extract_hashtags import extract_hashtags
            from Regex_Cheatsheet.extract_urls import extract_urls
            from Regex_Cheatsheet.find_phone_numbers import find_phone_numbers
            from Regex_Cheatsheet.validate_email import validate_email
            from Regex_Cheatsheet.remove_extra_spaces import remove_extra_spaces
            functions = {
                "upper-case": to_upper_case, "lower-case": to_lower_case,
                "sentence-case": to_sentence_case, "extract-dates": extract_dates,
                "extract-hashtags": extract_hashtags, "extract-urls": extract_urls,
                "find-phone-numbers": find_phone_numbers,
                "validate-email": validate_email, "remove-spaces": remove_extra_spaces,
            }
            return _text(functions[slug](text))
        if slug == "embed-youtube":
            if not re.fullmatch(r"[A-Za-z0-9_-]{11}", text.strip()):
                raise HTTPException(422, "Enter a valid 11-character YouTube video ID")
            return ("json", {"kind": "video", "result": text.strip()})
        if slug == "git-commands":
            return _text((ROOT / "Git_Utilities/Useful Git Commands.md").read_text(encoding="utf-8"))

        _check_files(slug, items)
        paths = []
        for index, (name, data) in enumerate(items):
            ext = Path(name).suffix.lower()
            path = root / f"upload_{index:03d}{ext}"
            path.write_bytes(data)
            paths.append(path)
        source = paths[0] if paths else None

        if slug in {"pdf-to-word", "pdf-to-images", "merge-pdfs", "split-pdf"}:
            for path in paths:
                _pdf_pages(path)
        if slug == "pdf-to-word":
            from File_Handling.convert_pdf_to_word import convert_pdf_to_word
            target = root / "converted.docx"
            convert_pdf_to_word(str(source), str(target))
            return _file(target.read_bytes(), target.name, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        if slug == "pdf-to-images":
            from File_Handling.convert_pdf_to_images import convert_pdf_to_images
            images = convert_pdf_to_images(str(source), dpi=_number(opts, "dpi", 120, 72, 200))
            output = io.BytesIO()
            with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
                for index, image in enumerate(images, 1):
                    data = io.BytesIO()
                    image.save(data, format="PNG")
                    archive.writestr(f"page_{index:03d}.png", data.getvalue())
            return _file(output.getvalue(), "pdf_images.zip", "application/zip")
        if slug == "word-to-pdf":
            from File_Handling.convert_word_doc_to_pdf import convert_word_doc_to_pdf
            target = root / "converted.pdf"
            convert_word_doc_to_pdf(str(source), str(target))
            return _file(target.read_bytes(), target.name, "application/pdf")
        if slug == "merge-pdfs":
            from File_Handling.merge_pdfs_in_folder import merge_pdfs_in_folder
            if len(paths) < 2:
                raise HTTPException(422, "Select at least two PDF files")
            if sum(_pdf_pages(path) for path in paths) > MAX_PDF_PAGES:
                raise HTTPException(422, f"Combined PDF limit is {MAX_PDF_PAGES} pages")
            target = root / "merged.pdf"
            merge_pdfs_in_folder(str(root), str(target))
            return _file(target.read_bytes(), target.name, "application/pdf")
        if slug == "split-pdf":
            from File_Handling.split_pdf import split_pdf
            folder = root / "pages"
            output_paths = split_pdf(str(source), str(folder))
            return _file(_make_zip([Path(p) for p in output_paths], folder), "split_pages.zip", "application/zip")
        if slug == "create-zip":
            output = io.BytesIO()
            with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
                for i, (name, data) in enumerate(items, 1):
                    archive.writestr(f"{i:03d}_{Path(name.replace(chr(92), '/')).name}", data)
            return _file(output.getvalue(), "archive.zip", "application/zip")
        if slug in {"extract-zip", "recursive-unzip"}:
            from File_Handling.archive_safety import validate_archive
            with zipfile.ZipFile(source) as archive:
                validated = validate_archive(archive)
                if slug == "extract-zip":
                    output = io.BytesIO()
                    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as result:
                        for member, member_name in validated:
                            if not member.is_dir():
                                result.writestr(member_name, archive.read(member))
                    return _file(output.getvalue(), "extracted_files.zip", "application/zip")
            from File_Handling.recursively_unzip_and_delete import unzip_and_delete
            extracted = [Path(p) for p in unzip_and_delete(str(root))]
            return _file(_make_zip(extracted, root), "unpacked_files.zip", "application/zip")

        if slug in {"grayscale-image", "compress-image", "convert-image", "resize-images"}:
            for path in paths:
                with Image.open(path) as im:
                    if im.width * im.height > MAX_PIXELS:
                        raise HTTPException(413, "Image dimensions exceed processing limit")
                    im.verify()
            if slug == "grayscale-image":
                from Image_Processing.convert_and_display_grayscale import convert_and_display
                target = root / "greyscale.png"
                convert_and_display(str(source), str(target))
                return _file(target.read_bytes(), target.name, "image/png")
            if slug == "compress-image":
                from Image_Processing.compress_image_by_percentage import compress_image_by_percentage
                percent = _number(opts, "percentage", 35, 1, 95)
                with Image.open(source) as im:
                    compressed = compress_image_by_percentage(im, percent)
                    output = Image.new("RGB", compressed.size, "white")
                    rgba = compressed.convert("RGBA")
                    output.paste(rgba, mask=rgba.getchannel("A"))
                    result = io.BytesIO()
                    output.save(result, format="JPEG", quality=85, optimise=True)
                return _file(result.getvalue(), "compressed.jpg", "image/jpeg")
            if slug == "convert-image":
                from Image_Processing.convert_image_format import convert_image_format
                fmt = str(opts.get("format", "PNG")).upper()
                if fmt not in {"PNG", "JPEG", "GIF"}:
                    raise HTTPException(422, "Choose PNG, JPEG or GIF")
                target = root / f"converted.{fmt.lower().replace('jpeg', 'jpg')}"
                convert_image_format(str(source), str(target), fmt)
                return _file(target.read_bytes(), target.name, "image/" + fmt.lower())
            if slug == "resize-images":
                percent = _number(opts, "percentage", 50, 1, 100)
                output = io.BytesIO()
                with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
                    for i, path in enumerate(paths, 1):
                        with Image.open(path) as im:
                            size = (
                                max(1, round(im.width * percent / 100)),
                                max(1, round(im.height * percent / 100)),
                            )
                            resized = im.resize(size, Image.Resampling.LANCZOS)
                            result = io.BytesIO()
                            fmt = "PNG" if path.suffix.lower() in {".png", ".webp", ".gif"} else "JPEG"
                            resized.save(result, format=fmt)
                        archive.writestr(f"{i:03d}.{fmt.lower().replace('jpeg', 'jpg')}", result.getvalue())
                return _file(output.getvalue(), "resized_images.zip", "application/zip")
        if slug == "notebook-to-python":
            from Jupyter_Notebook_Utilities.convert_notebook_to_clean_py import convert_notebook_to_clean_py
            target = root / "notebook.py"
            convert_notebook_to_clean_py(str(source), str(target))
            return _file(target.read_bytes(), "notebook.py", "text/x-python")
        if slug == "text-to-speech":
            from Audio_Speech_Processing.text_to_speech import text_to_speech
            if not text.strip() or len(text) > 2000:
                raise HTTPException(422, "Enter between 1 and 2,000 characters")
            rate = _number(opts, "rate", 160, 70, 260)
            voice = str(opts.get("voice", "male"))
            if voice not in {"male", "female"}:
                raise HTTPException(422, "Invalid voice")
            target = root / "speech.wav"
            text_to_speech(text, int(voice == "female"), rate, str(target))
            return _file(target.read_bytes(), "speech.wav", "audio/wav")
        if slug == "pitch-analysis":
            from Audio_Speech_Processing.analyse_pitch import analyse_pitch
            return ("json", {"kind": "json", "result": analyse_pitch(str(source))})
        raise HTTPException(501, "This tool is not available through the browser")


@app.post("/api/tools/{slug}/run")
async def run_tool(
    slug: str,
    files: list[UploadFile] | None = File(default=None),
    text: str = Form(default=""),
    options: str = Form(default="{}"),
):
    tool = TOOL_BY_SLUG.get(slug)
    if tool is None:
        raise HTTPException(404, "Unknown tool")
    if tool.local_only:
        raise HTTPException(403, "This operation is not exposed through the public API")
    uploaded = []
    total = 0
    try:
        for item in files or []:
            data = await item.read(MAX_FILE + 1)
            if len(data) > MAX_FILE:
                raise HTTPException(413, "Individual files must be 20 MiB or smaller")
            total += len(data)
            if total > MAX_TOTAL:
                raise HTTPException(413, "Uploaded files exceed the 40 MiB limit")
            filename = Path((item.filename or "upload").replace("\\", "/")).name
            uploaded.append((filename, data))
        validated_options = _options(options)
        try:
            await asyncio.wait_for(PROCESS_SLOTS.acquire(), timeout=0.3)
        except asyncio.TimeoutError as exc:
            raise HTTPException(429, "Processing capacity reached. Please try again.") from exc
        try:
            result = await run_in_threadpool(_execute, slug, uploaded, text, validated_options)
        finally:
            PROCESS_SLOTS.release()
    except HTTPException:
        raise
    except (ValueError, zipfile.BadZipFile, UnidentifiedImageError) as exc:
        raise HTTPException(422, "The supplied input could not be processed") from exc
    except Exception as exc:
        logger.exception("Tool failed: %s", slug)
        raise HTTPException(500, "Processing failed. Check the input and try again.") from exc
    finally:
        for item in files or []:
            await item.close()
    if result[0] == "json":
        return JSONResponse(result[1])
    _, data, filename, mime = result
    return Response(
        data,
        media_type=mime,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Utility-Filename": filename,
            "Cache-Control": "no-store",
        },
    )


# The app ships with its own prebuilt, same-origin frontend. Never expose
# project files or the user's filesystem through a generic static mount.
if (DIST / "assets").is_dir():
    app.mount("/assets", StaticFiles(directory=DIST / "assets"), name="assets")


@app.get("/", include_in_schema=False)
def index():
    if not (DIST / "index.html").is_file():
        raise HTTPException(503, "Frontend build missing")
    return FileResponse(DIST / "index.html", media_type="text/html")


@app.get("/{path:path}", include_in_schema=False)
def spa_route(path: str):
    if path.startswith(("api/", "assets/")) or "." in path or ".." in path:
        raise HTTPException(404, "Not found")
    return index()
