import os
from PIL import Image, ImageFont, ImageDraw

def add_caption(
    image_path,
    top_text="TOP TEXT",
    bottom_text="BOTTOM TEXT",
    font_path=None,
    font_size=140
):
    """
    Open the image at `image_path`, draw `top_text` and `bottom_text`
    (centered), and return the resulting PIL Image object.
    """

    # 1) Load image & prepare to draw
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # 2) Pick a font: your TTF if available, else PIL’s default
    try:
        font = ImageFont.truetype(font_path or "arial.ttf", font_size)
    except (IOError, OSError):
        font = ImageFont.load_default()

    # 3) Draw the top text, centered
    bbox = draw.textbbox((0, 0), top_text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (img.width - w) // 2
    y = 10
    draw.text((x, y), top_text, font=font, fill="white")

    # 4) Draw the bottom text, re-measuring and centering
    bbox = draw.textbbox((0, 0), bottom_text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (img.width - w) // 2
    y = img.height - h - 10
    draw.text((x, y), bottom_text, font=font, fill="white")

    # 5) Return the edited image; let your Flask route save it
    return img
