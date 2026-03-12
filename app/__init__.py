import os
from flask import Flask
from .database import db
from .routes import main

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    upload_folder = os.path.join(basedir, "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    app.config["UPLOAD_FOLDER"] = upload_folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "instance", "invoices.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        os.makedirs(os.path.join(basedir, "instance"), exist_ok=True)
        db.create_all()

    app.register_blueprint(main)

    return app