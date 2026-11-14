from pathlib import Path

import nbformat
import pytest
from pypdf import PdfReader, PdfWriter

from File_Handling.generate_file_tree import generate_file_tree
from File_Handling.merge_pdfs_in_folder import merge_pdfs_in_folder
from File_Handling.split_pdf import split_pdf
from Jupyter_Notebook_Utilities.convert_notebook_to_clean_py import (
    convert_notebook_to_clean_py,
)


def create_pdf(path: Path, pages=1):
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=100, height=100)
    with path.open("wb") as handle:
        writer.write(handle)


def test_file_tree_returns_text(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "file.txt").write_text("hi")
    output = generate_file_tree(str(tmp_path))
    assert isinstance(output, str)
    assert "sub" in output and "file.txt" in output


def test_file_tree_rejects_missing_directory(tmp_path):
    with pytest.raises(NotADirectoryError):
        generate_file_tree(str(tmp_path / "missing"))


def test_split_pdf_creates_each_page(tmp_path):
    source = tmp_path / "source.pdf"
    create_pdf(source, 3)
    names = split_pdf(str(source), str(tmp_path / "pages"))
    assert len(names) == 3
    assert all(len(PdfReader(name).pages) == 1 for name in names)


def test_merge_skips_existing_output(tmp_path):
    create_pdf(tmp_path / "one.pdf")
    create_pdf(tmp_path / "two.pdf")
    destination = tmp_path / "merged.pdf"
    merge_pdfs_in_folder(str(tmp_path), str(destination))
    assert len(PdfReader(str(destination)).pages) == 2
    merge_pdfs_in_folder(str(tmp_path), str(destination))
    assert len(PdfReader(str(tmp_path / "merged.pdf")).pages) == 2


def test_notebook_conversion_returns_path(tmp_path):
    notebook = nbformat.v4.new_notebook(cells=[
        nbformat.v4.new_code_cell("print('hello')"),
    ])
    source = tmp_path / "demo.ipynb"
    nbformat.write(notebook, str(source))
    path = convert_notebook_to_clean_py(str(source))
    assert isinstance(path, str)
    assert "print('hello')" in Path(path).read_text()


def test_notebook_removes_ipython_magics():
    from Jupyter_Notebook_Utilities.convert_notebook_to_clean_py import clean_python_code

    code = "get_ipython().run_line_magic('matplotlib', 'inline')\nprint('ok')\n"
    assert clean_python_code(code) == "print('ok')"
