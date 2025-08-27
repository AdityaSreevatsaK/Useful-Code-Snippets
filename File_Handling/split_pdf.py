import os

from PyPDF2 import PdfReader, PdfWriter


def split_pdf(input_path, output_folder):
    """
    Description:
        Split a PDF file into individual pages and save each page as a separate PDF file.
        This function reads the input PDF, extracts each page, and writes it to a new PDF file
        in the specified output folder.

    Args:
        input_path (str): The path to the input PDF file to be split.
        output_folder (str): The folder where the individual page PDFs will be saved.

    Returns:
        None
    """
    os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

    reader = PdfReader(input_path)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        with open(os.path.join(output_folder, f"page_{i + 1}.pdf"), "wb") as f:
            writer.write(f)


# split_pdf('Input.pdf', 'output_pages')
