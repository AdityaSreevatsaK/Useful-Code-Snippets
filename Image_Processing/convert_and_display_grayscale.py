from typing import Any

import cv2
import matplotlib.pyplot as plt
from cv2 import Mat
from numpy import dtype, ndarray


def convert_and_display(image_path: str, output_path: str = "Grayscale.png") -> Mat | ndarray:
    """
        Description:
            Convert an image to grayscale, save it, and display both the images side by side.

        Args:
            image_path (str): The path to the input image.
            output_path (str, optional): The path to save the grayscale image. Defaults to "Grayscale.png".

        Returns:
            None
    """
    # Read the image
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, gray_image)

    # Convert BGR to RGB for correct color display in Matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Display images side by side
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(image_rgb)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(gray_image, cmap="gray")
    plt.title("Grayscale Image")
    plt.axis("off")

    plt.suptitle("Original Image vs Grayscale Image.")
    plt.show()
    return gray_image


# Example usage
# convert_and_display(image_path="Folder path", output_path='Grayscale.png')
