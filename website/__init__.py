from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "djskdhkgh"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    # app.config["CACHE_TYPE"] = "null"
    db.init_app(app)

    # import the name of the blueprint
    from .views import views

    # register blueprint w the flask app
    app.register_blueprint(views, url_prefix="/")

    from .models import Transactions, Categories, init_db

    with app.app_context():
        db.create_all()
        init_db()
    return app
