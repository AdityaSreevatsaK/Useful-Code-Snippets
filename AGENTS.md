# Utility Shelf: guide for maintainers and AI engineering agents

## Mission

Utility Shelf is a professional browser workspace built around **34 reusable
Python utilities**. It supports file, image, document, audio and text workflows.
Preserve the original functions and API compatibility; never trade safety or
test coverage for superficial visual changes.

## Current production architecture

- server.py is the FastAPI application. Uvicorn serves port **7860**.
- web/index.html and web/assets/ form a responsive frontend with native
  HTML, CSS and JavaScript. It needs no npm installation.
- dashboard_catalogue.py is the 34-tool metadata catalogue, shared with
  the old Streamlit implementation.
- Original Python packages implement the underlying conversion functions.
- Dockerfile installs required system dependencies; the app runs as UID 1000.
- Hugging Face Space metadata in README.md specifies sdk: docker and
  app_port: 7860.
- scripts/check_hf_space.py checks the exact deployed commit SHA and
  /api/health. GitHub Actions accepts `main` and `master` during migration, publishes the checked-out commit to the Hugging Face `main` branch, and checks the deployed SHA.
- app.py, dashboard_handlers.py and dashboard_style.py are legacy
  Streamlit implementation files, kept temporarily for rollback.
  They are **not** the production entrypoint.

See docs/PRODUCTION_ARCHITECTURE.md for route contracts, frontend behaviour,
system diagrams, security limits, tests, and rollback instructions.

## API boundaries

Only allow tools declared in dashboard_catalogue.py. Never accept arbitrary
server paths, Python expressions, URLs or shell commands as executable API
inputs. All tools marked local_only must return 403 to API execution
requests, **even if ENABLE_LOCAL_OPERATIONS=1** is set by mistake.

HTTP endpoints:
- GET /api/health
- GET /api/tools
- GET /api/tools/{slug}/source
- POST /api/tools/{slug}/run
- GET /, GET /tools/{slug}, GET /assets/... for the UI

The source viewer is based exclusively on pre-approved catalogue paths.
Uploads are limited to 20 MiB each, 40 MiB total, 30 files, 50 PDF pages
and 25 million image pixels. ZIP entry names and decompression limits
must be validated. File processing uses temporary directories and never
needs database credentials. Processing concurrency is capped.

## Product UX principles

The first objective is a legible, efficient professional tool workspace.
Both themes must ensure sufficient foreground/background contrast on text
areas, inputs, buttons, dropdowns, focus rings and notices. Avoid global CSS
selectors that inadvertently override native controls. Preserve keyboard
search (Ctrl+K or Command+K), responsive mobile navigation, meaningful
empty states, tool previews and visible results.

Favourites and recent-tool metadata are stored in browser localStorage.
User-generated contents, uploads and outputs **must not** be put there.
They remain ephemeral in the browser tab and server temporary directory.

## Development, checks and delivery

1. Branch from the current GitHub default branch (`main` until explicitly renamed to `master`). No unreviewed production changes.
2. Install Python 3.11 with requirements.txt and pytest, httpx and Ruff.
3. Run Ruff and the Python test suite.
4. Check JavaScript syntax with node --check web/assets/app.js.
5. Run tests/test_web_api.py and tests/test_integration_runtime.py.
6. CI performs Chrome desktop/mobile smoke tests and contrast checks,
   including screenshot artefacts, plus Docker build/health checks.
7. Keep Gitleaks and pip-audit checks green before merging a PR.
8. After merge, check Hugging Face RUNNING, expected Git SHA and HTTP 200
   from /api/health. Inspect the live embedded app before closing.

The historical secret.key exposure is **not** fixed by this redesign.
Rotate any real-world encryption keys and re-encrypt affected data. A
history rewrite requires explicit approval and coordination.

## Cautions and ongoing hardening

- Server-side processing of untrusted content is a security-sensitive
  workload. The concurrency cap does not provide full multi-tenant
  sandboxing or external request throttling.
- The current Docker image contains Streamlit dependencies for legacy
  test compatibility; remove them only in a separate tested PR.
- Do not publish private tokens or upload user data to third-party
  analytics products.
- Keep related changes in their own PRs, preserving rollback paths.
