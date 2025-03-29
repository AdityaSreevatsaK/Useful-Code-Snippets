from pdf2docx import Converter


def convert_pdf_to_word(pdf_file_path: str, word_file_path: str):
    """
        Description:
            This function is used to convert the PDF document to Word document.

        Args:
            pdf_file_path (str): The path to the PDF document to be converted.
            word_file_path (str): The path to save the Word document.

        Returns:
            None
    """
    cv = Converter(pdf_file_path)

    cv.convert(word_file_path, start=0, end=None)
    cv.close()


# Example usage
pdf_file = "Path to PDF file"
word_file = "Path to save Word file"
convert_pdf_to_word(pdf_file, word_file)
