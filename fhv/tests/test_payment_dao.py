import pytest
from fhv.dao.payment_dao import PaymentDAO
from fhv.models import Payment, PayByCredit, PayByDebit, Person, Customer
from fhv.exts import db
from decimal import Decimal


@pytest.fixture
def payment_dao():
    return PaymentDAO()


def test_add_new_payment_credit(init_database, payment_dao):
    new_payment = payment_dao.add_new_payment_credit(
        amount=100.0,
        customer_id=1,
        card_number="1234-5678-9012-3456",
        cardholder="John Doe",
        expiry="12/24",
        cvv="123"
    )

    assert new_payment is not None
    assert isinstance(new_payment, PayByCredit)
    assert new_payment.amount == 100.0


def test_add_new_payment_debit(init_database, payment_dao):
    new_payment = payment_dao.add_new_payment_debit(
        amount=50.0,
        customer_id=1,
        account_number="1111-2222-3333-4444",
        bank_name="Test Bank",
        payee="John Doe"
    )

    assert new_payment is not None
    assert isinstance(new_payment, PayByDebit)
    assert new_payment.amount == 50.0


def test_get_payment_list(init_database, payment_dao):
    payment1 = Payment(amount=100.0, customer_id=1)
    payment2 = Payment(amount=50.0, customer_id=2)
    db.session.add_all([payment1, payment2])
    db.session.commit()

    payments = payment_dao.get_payment_list()
    assert len(payments) >= 2

    customer_payments = payment_dao.get_payment_list(customer_id=1)
    assert len(customer_payments) == 1
    assert customer_payments[0].amount == 100.0
