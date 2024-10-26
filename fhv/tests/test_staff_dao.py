import pytest
from fhv.dao.staff_dao import StaffDAO
from fhv.models import Payment, PremadeBox, WeightedVeggie, PackVeggie, UnitVeggie
from fhv.exts import db


@pytest.fixture
def staff_dao():
    return StaffDAO()


def test_get_daily_sales_data(init_database, staff_dao):
    payment = Payment(amount=100, customer_id=1)
    db.session.add(payment)
    db.session.commit()

    result = staff_dao.get_daily_sales_data()
    assert result is not None
    assert len(result) > 0
    assert result[0].total_amount == 100


def test_get_weekly_sales_data(init_database, staff_dao):
    payment1 = Payment(amount=100, customer_id=1)
    payment2 = Payment(amount=150, customer_id=1)
    db.session.add_all([payment1, payment2])
    db.session.commit()

    result = staff_dao.get_weekly_sales_data()
    assert result is not None
    assert len(result) > 0
    assert result[0].total_amount == 250


def test_count_most_popular_box_size(init_database, staff_dao):
    box1 = PremadeBox(box_size="Small Box", num_of_boxes=1)
    box2 = PremadeBox(box_size="Small Box", num_of_boxes=1)
    db.session.add_all([box1, box2])
    db.session.commit()

    result = staff_dao.count_most_popular_box_size([box1, box2])
    assert result['type'] == 'Small Box'
    assert result['count'] == 2


def test_count_most_popular_weighted_veggie(init_database, staff_dao):
    veggie1 = WeightedVeggie(name="Carrot", price_per_kilo=1.5, weight=5)
    veggie2 = WeightedVeggie(name="Carrot", price_per_kilo=1.5, weight=3)
    db.session.add_all([veggie1, veggie2])
    db.session.commit()

    result = staff_dao.count_most_popular_weighted_veggie([veggie1, veggie2])
    assert result['name'] == "Carrot"
    assert result['total_weight'] == 8


def test_count_most_popular_packed_veggie(init_database, staff_dao):
    veggie = PackVeggie(name="Lettuce", price_per_pack=1.5, num_of_packs=5)
    db.session.add(veggie)
    db.session.commit()

    result = staff_dao.count_most_popular_packed_veggie([veggie])
    assert result['name'] == "Lettuce"
    assert result['total_packs'] == 5


def test_count_most_popular_unit_veggie(init_database, staff_dao):
    veggie = UnitVeggie(name="Apple", price_per_unit=1.5, quantity=10)
    db.session.add(veggie)
    db.session.commit()

    result = staff_dao.count_most_popular_unit_veggie([veggie])
    assert result['name'] == "Apple"
    assert result['total_units'] == 10
