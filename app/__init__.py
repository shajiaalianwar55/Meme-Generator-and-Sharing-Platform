# app/__init__.py
from flask import Flask
from .db import db  
def create_app(test_config=None):
    app = Flask(__name__)

    # Default config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/database.db"  
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Test overrides
    if test_config:
        app.config.update(test_config)

    # Initialize DB
    db.init_app(app)

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app
