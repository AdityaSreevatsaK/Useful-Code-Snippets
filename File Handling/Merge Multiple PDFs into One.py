import os

from PyPDF2 import PdfMerger


def merge_pdfs_in_folder(folder_path, output_path):
    """
    Description:
        Merge multiple PDF files in a folder into a single PDF.
        This function iterates through all the files in the specified folder,
        identifies files with a `.pdf` extension, and merges them in sorted order
        into a single output PDF file.

    Args:
        folder_path (str): The path to the folder containing the PDF files to merge.
        output_path (str): The path where the merged PDF file will be saved.

    Returns:
        None
    """
    merger = PdfMerger()
    for file in sorted(os.listdir(folder_path)):
        if file.endswith(".pdf"):
            merger.append(os.path.join(folder_path, file))
    merger.write(output_path)
    merger.close()


merge_pdfs_in_folder('folder_path', 'Merged Document.pdf')
