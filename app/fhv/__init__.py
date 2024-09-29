from flask import Flask
from fhv.exts import db
from .config import DevelopmentConfig
from .blueprints.user import bp as user_bp
from .models import Customer, Staff, CorporateCustomer, Person


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(user_bp)

    return app
