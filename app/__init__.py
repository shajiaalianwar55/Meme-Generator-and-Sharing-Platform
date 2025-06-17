# app/__init__.py
from flask import Flask
from .db import db 
import os
def create_app(test_config=None):
    app = Flask(__name__)

    # Default config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    app.config['ALLOWED_EXTENSIONS']= ALLOWED_EXTENSIONS

    # Test overrides
    if test_config:
        app.config.update(test_config)

    # Initialize DB
    db.init_app(app)

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app
