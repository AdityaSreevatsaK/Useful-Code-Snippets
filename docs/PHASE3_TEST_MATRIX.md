# Phase 3 QA matrix

The latest PR checks are the source of truth, not a one-time declaration of
production readiness.

| Area | Automated checks | Additional manual or browser checks |
| --- | --- | --- |
| PDF splitting/merging | Page counts, output exclusion | Download ZIP and open files |
| PDF to images | Poppler output | Large and malformed PDFs |
| DOCX ↔ PDF | LibreOffice and reverse conversion | Fonts, tables and images |
| ZIP compression/extraction | Nested ZIP, traversal, bombs, overwrites | Download archive in browser |
| Audio and speech | Speech WAV, voiced pitch | Browser playback and voice choice |
| Images | Resize, transparency, GIF animation, greyscale | Visual quality and alpha |
| Notebook conversion | Code cells and magic removal | Complex notebooks with magics |
| Regex tools | Text transformations and extractors | Text entry, results and validation |
| Git, filesystem, HF | Disabled on public dashboard | Trusted local-only opt-in |
| Security | Gitleaks on current tree, pip-audit | Historical secrets and system packages |
| Deployment | Python tests, Docker build, HF health probe | Open live Space and test uploads |

## Test commands

```shell
python -m pip install -r requirements.txt pytest ruff pip-audit
ruff check .
python -m pytest -q --ignore=tests/test_integration_runtime.py
```

The Linux integration checks need Poppler, LibreOffice, eSpeak and FFmpeg.
CI installs these tools. Windows or macOS must supply equivalent tools.

Do not merge production changes while CI has failing checks. New major
dependencies are upgraded within the Docker build and deployment checks.
