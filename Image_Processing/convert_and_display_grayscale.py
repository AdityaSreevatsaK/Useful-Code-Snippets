"""Save and return a greyscale image for use in scripts or Streamlit."""

import cv2
import numpy as np


def convert_and_display(image_path: str, output_path: str = "Grayscale.png") -> np.ndarray:
    """Convert to greyscale without starting a Matplotlib window.

    The Streamlit dashboard displays the returned image directly.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Unable to decode image")
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if not cv2.imwrite(output_path, grayscale):
        raise OSError(f"Failed to write greyscale image: {output_path}")
    return grayscale
