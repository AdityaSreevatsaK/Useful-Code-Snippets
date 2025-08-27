import os
import re

import nbformat
from nbconvert import PythonExporter


def clean_python_code(code):
    """
    Clean Python code by removing unnecessary or unwanted elements.

    This function performs the following operations:
    - Remove cell markers like "# In[1]:"
    - Removes IPython magic commands (lines starting with `%` or `!`).
    - Comments out pip install lines (e.g., pip install ...)
    - Strips trailing spaces or other formatting issues.

    Parameters:
    code (str): The Python code to clean.

    Returns:
    str: The cleaned Python code.
    """
    # Remove cell markers like "# In[1]:"
    code = re.sub(r'^#\s*In\[\d*]:.*$', '', code, flags=re.MULTILINE)

    # Remove IPython magic commands (lines starting with % or !)
    code = re.sub(r'^\s*%.*$', '', code, flags=re.MULTILINE)
    code = re.sub(r'^\s*!.*$', '', code, flags=re.MULTILINE)

    # Comment out pip install lines (even if not starting with ! or %)
    code = re.sub(r'^(?!#)(.*\bpip\s+install\b.*)$', r'# \1', code, flags=re.MULTILINE)

    # Strip trailing whitespace
    code = re.sub(r'[ \t]+$', '', code, flags=re.MULTILINE)

    # Reduce multiple blank lines to a single blank line
    code = re.sub(r'\n{3,}', '\n\n', code)

    return code.strip()


def convert_notebook_to_clean_py(ipynb_path, output_py_path=None):
    """
    Convert a Jupyter Notebook to a cleaned Python script.

    This function reads a Jupyter Notebook file, converts its content to Python code,
    cleans the code by removing unnecessary elements (e.g., IPython magic commands),
    and writes the cleaned code to a Python (.py) file.

    Parameters:
    ipynb_path (str): The path to the input Jupyter Notebook file (.ipynb).
    output_py_path (str): The path to the output Python file (.py).

    Returns:
    None

    Side Effects:
    - Writes the cleaned Python code to the specified output file.
    - Prints a success message with the output file path.

    Example:
    convert_notebook_to_clean_py("notebook.ipynb", "clean_script.py")
    """
    # Load the notebook
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Export to Python code
    exporter = PythonExporter()
    source_code, _ = exporter.from_notebook_node(nb)

    # Clean the code
    cleaned_code = clean_python_code(source_code)

    # Derive cleaned output filename if not provided
    if output_py_path is None:
        base_name = os.path.basename(ipynb_path)
        name_without_ext = os.path.splitext(base_name)[0]
        output_py_path = os.path.join(os.path.dirname(ipynb_path), f"Cleaned_{name_without_ext}.py")

    # Write cleaned code
    with open(output_py_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_code)

    print(f"Notebook converted and cleaned successfully: {output_py_path}")
    return open(output_py_path, 'r', encoding='utf-8')
