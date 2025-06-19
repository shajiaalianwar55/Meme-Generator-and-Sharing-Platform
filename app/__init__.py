# app/__init__.py
from flask import Flask
from .db import db
import os

def create_app(test_config=None):
    app = Flask(__name__)

    # --- DATABASE: point at project_root/data/database.db ---
    # project_root = one level above this file (i.e. the folder containing "app/")
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    data_dir     = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)

    db_path = os.path.join(data_dir, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI']        = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- UPLOADS ---
    upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER']      = upload_folder
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

    # --- TEST OVERRIDES ---
    if test_config:
        app.config.update(test_config)

    # --- INIT & BLUEPRINTS ---
    db.init_app(app)
    from .routes import main
    app.register_blueprint(main)

    return app
