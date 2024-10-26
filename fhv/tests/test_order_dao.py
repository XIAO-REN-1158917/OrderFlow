import pytest
from fhv.dao.order_dao import OrderDAO
from fhv.models import Order, OrderItem, Item, Veggies
from fhv.exts import db
from decimal import Decimal


@pytest.fixture
def order_dao():
    return OrderDAO()


def test_check_draft_order(init_database, order_dao):
    order = Order(customer_id=1)
    db.session.add(order)
    db.session.commit()

    result = order_dao.check_draft_order(1)
    assert result is not None
    assert result.status == 'draft'


def test_get_order_items_by_order_id(init_database, order_dao):
    order = Order(customer_id=1)
    db.session.add(order)
    db.session.flush()

    item = Item(type="veggies")
    db.session.add(item)
    db.session.flush()

    order_item = OrderItem(item_id=item.id, item_price=5.0, order_id=order.id)
    db.session.add(order_item)
    db.session.commit()

    result = order_dao.get_order_items_by_order_id(order.id)
    assert len(result) == 1
    assert result[0]['item_price'] == 5.0


def test_add_item_to_order(init_database, order_dao):
    order = Order(customer_id=1)
    db.session.add(order)
    db.session.flush()

    item = Item(type="veggies")
    db.session.add(item)
    db.session.flush()

    order_dao.add_item_to_order(item.id, 3.5, order.id)

    result = OrderItem.query.filter_by(order_id=order.id).first()
    assert result is not None
    assert result.item_price == 3.5


def test_update_order_amount(init_database, order_dao):
    order = Order(customer_id=1, order_price=Decimal('10.00'))
    db.session.add(order)
    db.session.commit()

    order_dao.update_order_amount(order.id, 5.0)

    updated_order = Order.query.get(order.id)
    assert updated_order.order_price == Decimal('15.00')


def test_toggle_order_delivery_status(init_database, order_dao):
    order = Order(customer_id=1, is_delivery=False)
    db.session.add(order)
    db.session.commit()

    order_dao.toggle_order_delivery_status(order)
    assert order.is_delivery is True

    order_dao.toggle_order_delivery_status(order)
    assert order.is_delivery is False


def test_get_order_list(init_database, order_dao):
    order1 = Order(customer_id=1)
    order2 = Order(customer_id=1)
    db.session.add_all([order1, order2])
    db.session.commit()

    result = order_dao.get_order_list(customer_id=1)
    assert len(result) == 2


def test_get_order_by_id(init_database, order_dao):
    order = Order(customer_id=1)
    db.session.add(order)
    db.session.flush()

    result = order_dao.get_order_by_id(order.id)
    assert result is not None
    assert result.status == 'draft'
