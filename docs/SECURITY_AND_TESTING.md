# Security, processing limits and verification

## Public web safety

Utility Shelf v3 uses a **FastAPI** backend served by Uvicorn on port 7860.
The frontend is in web/. Privileged operations are not available over HTTP:
Git status, local filesystem inspection, arbitrary URL checks, tokens,
Hugging Face deletion and local logging are viewable as source reference
material only. FastAPI returns 403 regardless of ENABLE_LOCAL_OPERATIONS.

The old Streamlit dashboard has been retained for rollback only. If used
on a trusted local machine, never expose ENABLE_LOCAL_OPERATIONS=1 on a
public interface. The current public Space does not execute those handlers.

## Upload and execution limits

- Up to 20 MiB per uploaded file and 40 MiB per request.
- Up to 30 files per request, and 50 PDF pages per processing operation.
- Images above 25 million pixels are refused.
- ZIP validation rejects absolute and traversal paths, symlinks,
  duplicates, encrypted members and suspicious compression ratios.
- ZIP extraction is capped at five nested rounds and 100 MiB.
- Processing happens in separate temporary directories, which are
  cleaned up after the response data has been assembled.
- At most two concurrent processing operations run in each process.
  Excess jobs fail quickly with HTTP 429 instead of an unbounded queue.

These are safeguards, not a promise of hardened multi-tenant isolation.
Large-scale public hosting still requires external rate limiting,
request-body enforcement at the reverse proxy, workload quotas, security
patching and stronger isolation for document converters.

## Web security and privacy

The API rejects cross-origin POST requests when an Origin is present.
Responses set no-sniff, CSP, permissions and referrer policies.
The Content Security Policy explicitly allows framing by huggingface.co,
as needed for Space embedding. Do not introduce X-Frame-Options:
SAMEORIGIN, which would break embedded Space display.

No account or database is required. User content is processed temporarily.
Favourites and recent tool names are stored in localStorage; files and
generated data are not intentionally persisted there. Never record
uploaded file contents, credentials or personal information in logs.

## Historical encryption key

A Fernet-style secret.key existed in this repository's historical commits.
It has been removed from the current tree, but not history. Treat it as
compromised if it was used. Rotate the key and re-encrypt affected data.
Any history rewrite requires a separate coordinated recovery plan.

## Testing

Python 3.11/3.12 checks cover importability, AST parsing, linting,
unit tests and API contract tests. Linux integration exercises PDF,
DOCX, ZIP, image and audio utilities. Docker smoke checks port 7860,
GET /api/health, catalogue and frontend assets. Chromium smoke tests
exercise search, routes, text execution, mobile navigation and a dark
textarea contrast threshold of 7:1; desktop and mobile screenshots
are uploaded as CI artefacts.

Gitleaks scans the current checkout and pip-audit validates dependencies.
The deploy workflow uses the exact expected Git revision and /api/health.
Historical keys, OS-level vulnerabilities and sophisticated abuse are
not ruled out by these checks.
