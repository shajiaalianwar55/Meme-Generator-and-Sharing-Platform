from app.utils import add_caption  
import os

add_caption(
    image_path="testing_images/cat.jpg",
    top_text="Hello",
    bottom_text="cat",
    output_path = os.path.join(os.path.dirname(__file__),"..", "app", "static", "memes", "second.jpg")

)
