import os
from PIL import Image, ImageFont, ImageDraw

def add_caption(image_path, output_path, top_text="TOP TEXT", bottom_text="BOTTOM TEXT"):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", size=140)

    image_width = img.width

    # TOP TEXT
    bbox_top = draw.textbbox((0, 0), top_text, font=font)
    text_width = bbox_top[2] - bbox_top[0]
    text_height = bbox_top[3] - bbox_top[1]
    x = (image_width - text_width) / 2
    draw.text((x, 10), top_text, font=font, fill="white")

    # BOTTOM TEXT
    image_height = img.height
    bbox_bottom = draw.textbbox((0, 0), bottom_text, font=font)
    text_width = bbox_bottom[2] - bbox_bottom[0]
    text_height = bbox_bottom[3] - bbox_bottom[1]
    y = image_height - text_height - 10
    draw.text((x, y), bottom_text, font=font, fill="red")
    
    print("Resolved output path:", os.path.abspath(output_path))
    print("Saving to:", output_path)
    img.save(output_path)
    img.show()

