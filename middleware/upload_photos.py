import base64
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify


def upload_image(image_file):

    image = Image.open(image_file)
    image_format = image.format
    buffered = BytesIO()
    image.save(buffered, format=image_format)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    data_url = f"data:image/{image_format.lower()};base64,{img_str}"

    return data_url
