from decimal import Decimal
from typing import List, Optional

from flask import session
from sqlalchemy import desc
from fhv.exts import db
from sqlalchemy.orm import joinedload
from fhv.models import Payment, PayByCredit, PayByDebit
from sqlalchemy.orm import aliased


class PaymentDAO:
    def update_balance(self, order_price, user):
        order_price = Decimal(order_price)
        user.balance = user.balance+order_price
        db.session.commit()
        session['balance'] = user.balance

    def add_new_payment_credit(self, amount, customer_id, card_number, cardholder, expiry, cvv):
        new_payment = PayByCredit(
            amount, customer_id, card_number, cardholder, expiry, cvv)
        db.session.add(new_payment)
        db.session.commit()
        return new_payment

    def add_new_payment_debit(self, amount, customer_id, account_number, bank_name, payee):
        new_payment = PayByDebit(
            amount, customer_id, account_number, bank_name, payee)
        db.session.add(new_payment)
        db.session.commit()
        return new_payment

    def get_payment_list(self, customer_id: Optional[int] = None) -> List[Payment]:
        query = Payment.query.order_by(desc(Payment.created_at))
        if customer_id is not None:
            query = query.filter_by(customer_id=customer_id)
        return query.all()
