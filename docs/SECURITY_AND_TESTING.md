# Security, limitations and testing

## Hosted versus local operations

The public Streamlit dashboard deliberately disables:
- filesystem and Git-status inspection on the server;
- URL status probing;
- forms for personal GitHub/Hugging Face tokens;
- Hugging Face folder deletion.

To enable these utilities on a **trusted local machine only**:

On Linux/macOS:
    ENABLE_LOCAL_OPERATIONS=1 streamlit run app.py

On Windows PowerShell:
    $env:ENABLE_LOCAL_OPERATIONS = "1"
    streamlit run app.py

Never configure this setting on a publicly accessible Space or server.

## File uploads

- Files above 20 MiB are rejected; the Streamlit server also sets this limit.
- ZIP extraction rejects absolute/traversal paths, symlinks, overwrites,
  excessive decompressed sizes and suspicious compression ratios.
- ZIP extraction is limited to five nested archive rounds and 100 MiB.
- Conversions use temporary directories and remove temporary source files.
- Running arbitrary document converters on public uploads still warrants
  container resource limits, timeouts and rate limiting.

## Exposed encryption key

A Fernet-style file named `secret.key` was previously committed to this
public repository. This branch deletes it and adds it to `.gitignore`, but
it remains in Git history and on the production branch until merged.
Treat it as compromised if it was ever used with sensitive material.
Rotate the key and re-encrypt any data that must remain confidential.
Any optional history rewrite requires deliberate coordination with clones.

## Operating system dependencies

PDF-to-image conversion requires Poppler.
Linux DOCX-to-PDF requires LibreOffice.
Text-to-speech requires a supported speech engine and installed voices.
The available voice genders and audio output formats vary by platform.

## Verification

The quality workflow runs on Python 3.11 and Python 3.12.
It checks code compilation and regression tests for archives, PDFs,
notebook conversion, images and local-only UI contract checks.

Run locally:
    python -m pip install pytest Pillow PyPDF2 pdf2image nbformat nbconvert
    python -m pytest -q

The offline tests do not exercise every OS-specific conversion or the
publicly hosted application. Integration checks remain necessary before merge.

## Outstanding work

- Update and audit pinned third-party dependency versions.
- Verify the Hugging Face Space builds with Poppler, LibreOffice and speech
  engine packages before merging.
- Consider a separate local-only CLI for privileged utilities.
- The DNS validation in website status checks is not a sufficient defence
  for a general-purpose public URL fetcher. Keep it local-only.
