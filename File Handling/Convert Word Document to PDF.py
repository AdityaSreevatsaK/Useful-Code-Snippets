from docx2pdf import convert


def convert_word_doc_to_pdf(word_folder_path: str, pdf_folder_path: str = None):
    """
        Description: This function is used to convert the Word document to PDF.

        Args:
            word_folder_path (str): The path to the folder containing the Word document(s) to be converted.
            pdf_folder_path (str, optional): The path to the folder where the converted PDF(s) will be saved.
                                             Defaults to None.

        Returns:
            None
    """
    convert(input_path=word_folder_path, output_path=pdf_folder_path)


docx_file_path = "Path to Word document"
pdf_file_path = "Path to save PDF file"
convert_word_doc_to_pdf(docx_file_path, pdf_file_path)
