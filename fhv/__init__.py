from flask import Flask
from fhv.exts import db
from .config import DevelopmentConfig
from .blueprints.user import bp as user_bp
from fhv.blueprints.staff import bp as staff_bp
from fhv.blueprints.customer import bp as customer_bp
from .models import Person, Customer, Staff, CorporateCustomer


def create_app(config_class=None):
    # The settings here are for testing convenience.
    # When a test configuration is passed in, the test configuration is used.
    # Otherwise, the normal development configuration is used.
    if config_class is None:
        config_class = DevelopmentConfig
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(customer_bp)

    return app
