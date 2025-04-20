from PIL import Image


def convert_image_format(input_path, output_path, image_format='JPEG'):
    if not output_path.lower().endswith(f".{image_format.lower()}"):
        output_path += f".{image_format.lower()}"
    image = Image.open(input_path).convert("RGB")
    image.save(output_path, format=image_format)


convert_image_format("input_path.jpg", "output_path.jpeg", 'JPEG')
