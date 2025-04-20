import os

from PIL import Image


def resize_all_images_in_folder(folder_path, percentage):
    """
    Description:
        Resize all images in a folder by a specified percentage.
        This function iterates through all image files in the given folder, resizes
        each image to the specified percentage of its original dimensions, and
        saves the resized image back to its original file path.

    Args:
        folder_path (str): The path to the folder containing the images.
        percentage (float): The percentage to which the images should be resized.

    Returns:
        None
    """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, filename)
            img = Image.open(full_path)
            new_size = (int(img.width * percentage / 100), int(img.height * percentage / 100))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            img.save(full_path)


resize_all_images_in_folder("folder_path", 50)
