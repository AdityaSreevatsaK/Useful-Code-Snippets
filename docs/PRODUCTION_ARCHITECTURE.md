# Utility Shelf v3: Engineering and architecture guide

## Product goal

Utility Shelf is a focused, professional browser interface for independently
reusable Python utilities. The product intentionally avoids the familiar
Streamlit notebook/dashboard appearance: it has an explicit layout, accessible
design tokens, search and navigation, reusable input/output panels, and
source-code inspection.

## Runtime design

- The Hugging Face Space runs a single Python 3.11 Docker container.
- Uvicorn serves the FastAPI application in server.py on port 7860.
- The API serves the static, dependency-free frontend from web/.
- GET /api/health is the deployment readiness endpoint.
- GET /api/tools returns a fixed 34-tool catalogue.
- GET /api/tools/{slug}/source reads **only a registry-approved source file**.
- POST /api/tools/{slug}/run dispatches approved conversions and text tools.
- All utility implementations remain in their existing Python modules.
- Legacy Streamlit UI files are retained for rollback reference only.

## Frontend structure

- web/index.html: semantic shell, local CSS and JS.
- web/assets/styles.css: component-level design tokens and two contrast-tested
  palettes. Dark mode **always** controls backgrounds and text in inputs.
- web/assets/app.js: navigation, search, catalogue, favourites, recent tools,
  input validation, temporary outputs and the copyable source viewer.
- web/assets/favicon.svg: vector brand mark.

Search can be launched with Ctrl+K or Command+K. Users can filter by collection,
save favourites and reopen recently used tools. Browser favourites and history
are stored in localStorage. Private text, uploaded files and generated output
are held **only in browser memory**, never localStorage.

URL routes use /tools/{slug}; browser back/forward is supported. The server
serves the SPA entrypoint at those routes, and never allows arbitrary files
to be read through a catch-all static route.

## Public API security

Privileged tools are marked local_only in dashboard_catalogue.py and rejected
with HTTP 403 by the server regardless of environment variables. This includes
Hugging Face deletion, arbitrary URL requests, Git authentication and server
filesystem inspection. Such tools remain viewable as source references.

File limits: 20 MiB per file, 40 MiB per request and 30 files. PDF operations
check page limits. Image operations check pixel limits. ZIP operations use
centralised path, decompression size, ratio and symlink validation. Only
expected output types are exposed. The server does not store uploaded data
between requests and does not expose arbitrary filesystem paths.

HTTP responses set CSP, no-sniff, permissions policy and referrer policy
headers. CSP allows framing by huggingface.co because the Space is an iframe;
do not set X-Frame-Options: SAMEORIGIN, which would break the deployment.
CORS is not enabled; cross-origin POST requests with an Origin header are
explicitly rejected. These measures do **not** replace external rate limiting,
resource quotas or abuse monitoring for a large-scale public service.

## Testing

- Portable checks: Python 3.11 and 3.12 compilation, Ruff and fast unit tests.
- Runtime checks: converters, images, speech, old UI compatibility and new API.
- Docker smoke: builds production image, validates /api/health and /api/tools
  and confirms frontend HTML and JavaScript are served.
- Gitleaks scans the current tree; pip-audit checks Python dependencies.
- After merging, GitHub Actions deploys the checked-out GitHub commit to the
  Hugging Face Space's `main` branch and confirms its exact Git SHA and HTTP
  /api/health response.

## Deployment and rollback

During the transition, deployment triggers on pushes to either GitHub `main` or
`master`. GitHub currently uses `main`; when its default branch is renamed to
`master`, deployment will continue to work without requiring a Hugging Face
branch rename. The workflow publishes the checked-out commit using
`git push hf HEAD:main`, keeping the Hugging Face Space on `main`.

Work on separate branches with PR checks; do not overwrite production or
force-push a Space unexpectedly. After verifying the renamed GitHub branch's
first successful deployment, remove the unused GitHub `main` trigger.
Because the previous Streamlit frontend remains in the repository, rollback
can be performed by reverting the v3 deployment commit, restoring the previous
Dockerfile, port and health endpoint. Validate the old container before a
production rollback.

## Current limitations

1. Browser testing with actual Chrome/Firefox, keyboard focus and mobile
   viewport screenshots should be reviewed before calling the UI pixel-perfect.
2. Heavy conversions need external concurrency limits for a high-traffic
   public service; the present server processes each request in a temporary
   workspace but is not a hardened multi-tenant sandbox.
3. The previously exposed encryption key remains in historical commits.
   Rotate it if it protected real encrypted data. This is not fixed by
   removing the current tree's key.
4. The old Streamlit dependencies remain temporarily to preserve legacy
   tests and a safe rollback path. Remove them in a separate cleanup release.
