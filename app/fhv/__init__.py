from flask import Flask
from fhv.exts import db
from .config import DevelopmentConfig
from .blueprints.user import bp as user_bp
from fhv.blueprints.staff import bp as staff_bp
from fhv.blueprints.customer import bp as customer_bp
from .models import Person, Customer, Staff, CorporateCustomer


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(customer_bp)

    return app
