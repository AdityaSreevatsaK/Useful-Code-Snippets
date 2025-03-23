from pdf2image import convert_from_path


# Additional requirement:
# Install Poppler. Download it from https://github.com/oschwartz10612/poppler-windows/releases/
# Extract the contents of the zip file and add the path to the bin folder to the system environment variable PATH.

def convert_pdf_to_images(folder_path: str):
    """
        Description: This function converts each page of a PDF file to images.
    """
    images = convert_from_path(folder_path)

    for i, image in enumerate(images):
        image.save(f'page_{i + 1}.png', 'PNG')


pdf_path = 'Folder path'
convert_pdf_to_images(pdf_path)
