from decimal import Decimal

from flask import session
from fhv.exts import db
from sqlalchemy.orm import joinedload
from fhv.models import Item, Veggies, PremadeBox, WeightedVeggie, PackVeggie, UnitVeggie, Order, OrderItem
from sqlalchemy.orm import aliased


class PaymentDAO:
    def update_balance(self, order_price, user):
        order_price = Decimal(order_price)
        user.balance = user.balance+order_price
        db.session.commit()
        session['balance'] = user.balance
