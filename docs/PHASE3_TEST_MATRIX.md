# Historical Phase 3 quality matrix

This file records the initial Streamlit-era hardening phase. The current
production app is **FastAPI + a standalone frontend**, not Streamlit.

For current deployment and testing practices, use:

- docs/PRODUCTION_ARCHITECTURE.md
- docs/SECURITY_AND_TESTING.md
- AGENTS.md
- tests/test_web_api.py
- scripts/browser_smoke.py

The initial Phase 3 fixes included protection against ZIP traversal,
PDF/office conversion failures, encryption key leakage, unsafe server
operations and dependency vulnerabilities. The corresponding regression
tests remain in the repository.

Current CI must pass Python 3.11/3.12 checks, Linux integration, Chrome UI
checks, Docker smoke, dependency audit and secret scanning before merging.
