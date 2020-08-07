import streamlit
from PIL import Image


def handle_image(path: str, width: int = 225, height: int = 225):
    image = Image.open(path)
    resized = image.resize((width, height))
    streamlit.image(resized)
