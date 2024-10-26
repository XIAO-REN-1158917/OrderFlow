import pytest
from fhv.dao.customer_dao import CustomerDAO
from fhv.models import Veggies, Person, PremadeBox
from fhv.exts import db


@pytest.fixture
def customer_dao():
    return CustomerDAO()


def test_get_veggie_by_name(init_database, customer_dao):
    veggie = customer_dao.get_veggie_by_name("Carrot")
    assert veggie is not None
    assert veggie.name == "Carrot"


def test_get_user_by_id(init_database, customer_dao):
    user = customer_dao.get_user_by_id(1)  # Assuming ID 1 exists
    assert user is not None
    assert user.id == 1


def test_add_weighted_veggie(init_database, customer_dao):
    new_veggie = customer_dao.add_weighted_veggie("Potato", 2.5, 1.0)
    assert new_veggie is not None
    assert new_veggie.name == "Potato"
    assert new_veggie.price_per_kilo == 2.5
    assert new_veggie.weight == 1.0


def test_add_pack_veggie(init_database, customer_dao):
    new_pack = customer_dao.add_pack_veggie("Lettuce", 1.5, 3)
    assert new_pack is not None
    assert new_pack.name == "Lettuce"
    assert new_pack.price_per_pack == 1.5
    assert new_pack.num_of_packs == 3


def test_add_unit_veggie(init_database, customer_dao):
    new_unit = customer_dao.add_unit_veggie("Apple", 0.5, 10)
    assert new_unit is not None
    assert new_unit.name == "Apple"
    assert new_unit.price_per_unit == 0.5
    assert new_unit.quantity == 10
