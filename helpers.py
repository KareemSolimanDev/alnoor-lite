import os ,secrets
from PIL import Image
from flask import current_app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/lesson-images/', picture_name)
    i = Image.open(form_picture)
    i.thumbnail((150,150))
    i.save(picture_path)
    return picture_name