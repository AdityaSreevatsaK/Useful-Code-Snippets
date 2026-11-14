---
title: Utility-Shelf
emoji: 📦
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

<!-- This metadata block is for Hugging Face Spaces -->

# Utility Shelf

**A professional workspace for practical Python utilities.**

[Live application](https://huggingface.co/spaces/AdityaSreevatsaK/Utility-Shelf) | [Architecture](docs/PRODUCTION_ARCHITECTURE.md) | [Security](SECURITY.md)

Utility Shelf offers 34 independent Python tools, searchable in a responsive application for files, images, audio, text and developer workflows.

## Product features

- Searchable catalogue and command launcher using Ctrl+K
- Dedicated workspaces, clear form controls, previews and downloads
- High-contrast light and dark themes with mobile-friendly layouts
- Favourites and recent tools saved locally in your browser
- Source-code viewer with copy support, linked to the standalone Python modules
- Upload processing in temporary directories, with no persistent file storage
- Privileged local utilities available as reference only, never through the public API

## Architecture

| Layer | Implementation |
| --- | --- |
| Frontend | HTML, CSS, modular browser JavaScript, no external frontend packages |
| API | FastAPI + Uvicorn, same-origin requests |
| Processing | Standalone Python utilities |
| Deployment | Python 3.11 Docker Space, port 7860 |
| Quality | API tests, Python regressions, Docker health, secret and dependency scanning |

The previous Streamlit dashboard is retained as legacy reference and a rollback option. **The deployed application runs FastAPI, not Streamlit.**

## Local development

Use Python 3.11.

1. Install dependencies: python -m pip install -r requirements.txt
2. Start the server: uvicorn server:app --host 127.0.0.1 --port 7860 --reload
3. Open http://127.0.0.1:7860

Some document and speech tools additionally require Poppler, LibreOffice, eSpeak and FFmpeg.

Run tests using pytest -q tests/test_web_api.py. See [architecture and operating notes](docs/PRODUCTION_ARCHITECTURE.md).

## Contributing

Preserve standalone APIs and add regression tests. Do not expose filesystem inspection, arbitrary URL access, tokens or destructive operations through the public web API. See [LICENSE](LICENSE).
