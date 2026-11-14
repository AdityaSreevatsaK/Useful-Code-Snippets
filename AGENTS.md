# Useful Code Snippets: project guide for maintainers and AI agents

## Purpose and boundaries

Useful Code Snippets is both a library of independently importable Python
utilities and a public Streamlit dashboard called **Utility-Shelf**.
Preserve snippets' importable function APIs unless changes are tested and
documented. Keep user-uploaded processing available on the hosted dashboard,
but keep privileged operations local-only.

## Sources of truth

- \`README.md\`: project index and Hugging Face Space YAML front matter.
- \`app.py\`: Streamlit user interface and section routing.
- \`requirements.txt\`: Python 3.11 runtime dependency pins.
- \`Dockerfile\`: Hugging Face Space container, non-root user, port 8501.
- \`.github/workflows/deploy.yml\`: pushes \`main\` to the live Space; health check.
- \`.github/workflows/integration.yml\`: Linux converters, Streamlit and Docker smoke tests.
- \`.github/workflows/quality.yml\`: portable Python tests and compilation.
- \`.github/workflows/security.yml\`: newly committed secrets and dependency audit.
- \`docs/SECURITY_AND_TESTING.md\`: deployment safety, limits and residual risks.

## Architecture

\`\`\`text
main branch (GitHub)
  ├── app.py (Streamlit)
  │   ├── Audio_Speech_Processing/
  │   ├── Automation_Productivity/
  │   ├── File_Handling/
  │   ├── Git_Utilities/
  │   ├── HuggingFace_Utilities/
  │   ├── Image_Processing/
  │   ├── Jupyter_Notebook_Utilities/
  │   └── Regex_Cheatsheet/
  ├── tests/ (unit and Linux integration)
  └── GitHub Actions deploy → Hugging Face Docker Space
\`\`\`

Functions should return useful values rather than print to server stdout.
The dashboard should handle errors and let users download generated files.
Convert documents inside temporary directories. Do not write uploaded paths
directly to host filenames or allow hostile ZIP members.

## High-risk controls

\`ENABLE_LOCAL_OPERATIONS=1\` enables filesystem inspection, URL probing,
Git operations and token-based Hugging Face deletion. Never enable it in
production or other publicly accessible deployments. GitHub and HF tokens
must remain request-scoped. No credentials belong in repo files.

The earlier public \`secret.key\` was removed from the current checkout,
**not historical commits**. It may require rotating any keys used by real
encrypted data and potentially re-encrypting datasets. Never rewrite Git
history or rotate private secrets without an impact plan and the owner's
explicit approval.

## Development and checks

1. Branch from \`main\`. Avoid direct production changes.
2. \`python -m pip install -r requirements.txt pytest ruff pip-audit\`
3. \`ruff check .\`
4. \`python -m pytest -q --ignore=tests/test_integration_runtime.py\`
5. Run Linux converter integration checks and build the Docker image in CI.
6. Review GitHub checks, then merge through a PR. This triggers production
   deployment and the post-push Space health check.

**Cost control:** CI runs on PRs rather than on both push and PR. Docker and
Linux smoke tests intentionally run on the same PR; avoid redundant reruns.

## Current Phase 3 focus

Modernise dependencies without breaking the working Docker environment,
add secret and dependency scanning, expand regression tests, remove tracked
IDE files, improve errors and type annotations, and document remaining risks.
The visual redesign is a separate Phase 4 and should not be mixed into
security-focused changes.
