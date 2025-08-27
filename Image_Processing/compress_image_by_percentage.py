from PIL import Image


def compress_image_by_percentage(image, percentage_to_compress):
    """
    Description:
        Compress an image by a specified percentage.
        This function resizes an image to a percentage of its original dimensions
        and saves the compressed image to the specified output path.

    Args:
        image: The image to be resized.
        percentage_to_compress (float): The percentage to which the image is compressed.

    Returns:
        None
    """
    width, height = image.size
    percentage_to_compress = 100 - percentage_to_compress
    new_width = int(width * (percentage_to_compress / 100))
    new_height = int(height * (percentage_to_compress / 100))

    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_image
