from datetime import date, datetime

from sqlalchemy import Numeric
from fhv.exts import db


class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type,
    }

    def __init__(self, firstname: str, lastname: str, username: str, password: str):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password

    def check_password(self, password: str) -> bool:
        return self.password == password


class Staff(Person):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    department = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    def __init__(self, firstname: str, lastname: str, username: str, password: str, department: str):
        super().__init__(firstname, lastname, username, password)
        self.department = department


class Customer(Person):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    balance = db.Column(Numeric(10, 2), default=0.0)
    address = db.Column(db.String(100), nullable=True)
    payments = db.relationship(
        'Payment', back_populates='customer', cascade='all, delete-orphan')
    orders = db.relationship(
        'Order', back_populates='customer', cascade='all, delete-orphan')
    max_owing = 100.0

    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }

    def __init__(self, firstname: str, lastname: str, username: str, password: str, address: str = None):
        super().__init__(firstname, lastname, username, password)
        self.address = address


class CorporateCustomer(Customer):
    __tablename__ = 'corporate_customer'
    id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    credit_limit = db.Column(Numeric(10, 2), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'corporate_customer',
    }

    def __init__(self, firstname: str, lastname: str, username: str, password: str, address: str, credit_limit: float):
        super().__init__(firstname, lastname, username, password, address)
        self.credit_limit = credit_limit


class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='payments')

    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'payment',
        'polymorphic_on': type,
    }

    def __init__(self, amount: Numeric, customer_id: int):
        self.amount = amount
        self.customer_id = customer_id


class PayByCredit(Payment):
    __tablename__ = 'pay_by_credit'
    id = db.Column(db.Integer, db.ForeignKey('payment.id'), primary_key=True)
    card_number = db.Column(db.String(50), nullable=False)
    cardholder = db.Column(db.String(20), nullable=False)
    expiry = db.Column(db.String(5), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'pay_by_credit',
    }

    def __init__(self, amount: float, customer_id: int, card_number: str, cardholder: str, expiry: str, cvv: str):
        super().__init__(amount, customer_id)
        self.card_number = card_number
        self.cardholder = cardholder
        self.expiry = expiry
        self.cvv = cvv


class PayByDebit(Payment):
    __tablename__ = 'pay_by_debit'
    id = db.Column(db.Integer, db.ForeignKey('payment.id'), primary_key=True)
    account_number = db.Column(db.String(50), nullable=False)
    bank_name = db.Column(db.String(20), nullable=False)
    payee = db.Column(db.String(20), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'pay_by_debit',
    }

    def __init__(self, amount: float, customer_id: int, account_number: str, bank_name: str, payee: str):
        super().__init__(amount, customer_id)
        self.account_number = account_number
        self.bank_name = bank_name
        self.payee = payee

    def __repr__(self):
        return (f"<PayByDebit(id={self.id}, amount={self.amount}, created_at={self.created_at}, "
                f"account_number={self.account_number}, bank_name={self.bank_name}, payee={self.payee}, customer_id={self.customer_id})>")


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_on': type,
    }

    order_items = db.relationship(
        'OrderItem', back_populates='item', cascade='all, delete-orphan')


class Veggies(Item):
    __tablename__ = 'veggies'
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'veggies',
    }

    def __init__(self, name: str):
        super().__init__()
        self.name = name


class WeightedVeggie(Veggies):
    __tablename__ = 'weighted_veggie'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    price_per_kilo = db.Column(Numeric(10, 2), nullable=False)
    weight = db.Column(Numeric(10, 2), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'weighted_veggie',
    }

    def __init__(self, name: str, price_per_kilo: Numeric, weight: Numeric):
        super().__init__(name)
        self.price_per_kilo = price_per_kilo
        self.weight = weight


class PackVeggie(Veggies):
    __tablename__ = 'pack_veggie'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    price_per_pack = db.Column(Numeric(10, 2), nullable=False)
    num_of_packs = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'pack_veggie',
    }

    def __init__(self, name: str, price_per_pack: Numeric, num_of_packs: int):
        super().__init__(name)
        self.price_per_pack = price_per_pack
        self.num_of_packs = num_of_packs


class UnitVeggie(Veggies):
    __tablename__ = 'unit_veggie'
    id = db.Column(db.Integer, db.ForeignKey('veggies.id'), primary_key=True)
    price_per_unit = db.Column(Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'unit_veggie',
    }

    def __init__(self, name: str, price_per_unit: Numeric, quantity: int):
        super().__init__(name)
        self.price_per_unit = price_per_unit
        self.quantity = quantity


class PremadeBox(Item):
    __tablename__ = 'premade_box'
    id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    box_size = db.Column(db.Enum('Small Box', 'Medium Box',
                         'Large Box'), name='premade_box_size', nullable=False)
    num_of_boxes = db.Column(db.Integer, nullable=False)

    content = []

    __mapper_args__ = {
        'polymorphic_identity': 'premade_box',
    }

    def __init__(self, box_size: str, num_of_boxes: int, content):
        super().__init__()
        self.box_size = box_size
        self.num_of_boxes = num_of_boxes
        self.content = content


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey(
        'item.id', ondelete='CASCADE'), nullable=False)
    item_price = db.Column(Numeric(10, 2), nullable=False)
    item = db.relationship('Item', back_populates='order_items')

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('Order', back_populates='order_items')

    def __init__(self, item_id: int, item_price: Numeric, order_id: int):
        self.item_id = item_id
        self.item_price = item_price
        self.order_id = order_id

    def __repr__(self):
        return f"<OrderItem(id={self.id}, item_id={self.item_id}, order_id={self.order_id})>"


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='orders')

    order_items = db.relationship(
        'OrderItem', back_populates='order', cascade='all, delete-orphan')

    order_date = db.Column(db.Date, nullable=False, default=date.today)
    is_delivery = db.Column(db.Boolean, nullable=False, default=False)

    status = db.Column(db.Enum('draft', 'pending', 'processing', 'completed', 'canceled', name='order_status'),
                       nullable=False, default='draft')
    order_price = db.Column(Numeric(10, 2), nullable=False, default=0.00)
    delivery_fee = 10.0

    def __init__(self, customer_id: int, is_delivery: bool = False, order_price: Numeric = 0.00):
        self.customer_id = customer_id
        self.is_delivery = is_delivery
        self.order_price = order_price

    def __repr__(self):
        return f"<Order(id={self.id}, customer_id={self.customer_id}, is_delivery={self.is_delivery}, status={self.status})>"
