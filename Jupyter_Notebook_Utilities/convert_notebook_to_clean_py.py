"""Convert notebook code cells into a clean Python script."""

from pathlib import Path
import re

import nbformat
from nbconvert import PythonExporter


def clean_python_code(code: str) -> str:
    code = re.sub(r"^#\s*In\[\d*]:.*$", "", code, flags=re.MULTILINE)
    code = re.sub(r"^\s*[%!].*$", "", code, flags=re.MULTILINE)
    code = re.sub(r"^(?!#)(.*\bpip\s+install\b.*)$", r"# \1", code, flags=re.MULTILINE)
    code = re.sub(r"[ \t]+$", "", code, flags=re.MULTILINE)
    return re.sub(r"\n{3,}", "\n\n", code).strip()


def convert_notebook_to_clean_py(ipynb_path: str, output_py_path: str | None = None) -> str:
    """Return the generated filename, rather than an open file handle."""
    source = Path(ipynb_path)
    notebook = nbformat.read(str(source), as_version=4)
    text, _ = PythonExporter().from_notebook_node(notebook)
    destination = Path(output_py_path) if output_py_path else source.with_name(f"Cleaned_{source.stem}.py")
    destination.write_text(clean_python_code(text), encoding="utf-8")
    return str(destination)
