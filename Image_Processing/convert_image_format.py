from PIL import Image


def convert_image_format(input_path, output_path, image_format='JPEG'):
    """
    Description:
        Convert the format of an image to a specified format.
        This function takes an input image file, converts it to the specified format,
        and saves it to the given output path.

    Args:
        input_path (str): The file path of the input image.
        output_path (str): The file path to save the converted image.
        image_format (str): The desired image format (default is 'JPEG').

    Returns:
        None
    """
    if not output_path.lower().endswith(f".{image_format.lower()}"):
        output_path += f".{image_format.lower()}"
    image = Image.open(input_path).convert("RGB")
    image.save(output_path, format=image_format)


# convert_image_format("input_path.jpg", "output_path.jpeg", 'JPEG')
