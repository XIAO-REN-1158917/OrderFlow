import pytest
from fhv import create_app
from fhv.exts import db
from fhv.models import Person, Veggies
from fhv.config import TestingConfig


@pytest.fixture
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_database(app):
    with app.app_context():
        person = Person(firstname='Bob', lastname='James',
                        username='pcustomer4', password='pcustomer123')
        db.session.add(person)
        carrot = Veggies(name="Carrot")
        db.session.add(carrot)
        db.session.commit()
