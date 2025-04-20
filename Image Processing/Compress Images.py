from PIL import Image


def compress_image_by_percentage(input_path, output_path, percentage_to_compress):
    """
    Description:
        Compress an image by a specified percentage.
        This function resizes an image to a percentage of its original dimensions
        and saves the compressed image to the specified output path.

    Args:
        input_path (str): The file path of the input image.
        output_path (str): The file path to save the compressed image.
        percentage_to_compress (float): The percentage to which the image is compressed.

    Returns:
        None
    """
    image = Image.open(input_path)
    width, height = image.size
    percentage_to_compress = 100 - percentage_to_compress
    new_width = int(width * (percentage_to_compress / 100))
    new_height = int(height * (percentage_to_compress / 100))

    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    resized_image.save(output_path, optimize=True, quality=85)


compress_image_by_percentage('input.jpg', 'output.jpg', 50)
