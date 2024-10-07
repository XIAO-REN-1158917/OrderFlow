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

    def __repr__(self):
        return f"<Person(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, username={self.username})>"


class Staff(Person):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    department = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    def __init__(self, department: str, **kwargs):
        super().__init__(**kwargs)
        self.department = department

    def __repr__(self):
        return f"<Staff(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, department={self.department})>"


class Customer(Person):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    balance = db.Column(Numeric(10, 2), default=0.0)
    address = db.Column(db.String(100), nullable=True)
    max_owing = db.Column(Numeric(10, 2), default=100.0)
    payments = db.relationship(
        'Payment', back_populates='customer', cascade='all, delete-orphan')
    orders = db.relationship(
        'Order', back_populates='customer', cascade='all, delete-orphan')

    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }

    def __init__(self, address: str = None, **kwargs):
        super().__init__(**kwargs)
        self.address = address

    def __repr__(self):
        return f"<Customer(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, balance={self.balance})>"


class CorporateCustomer(Customer):
    __tablename__ = 'corporate_customer'
    id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    credit_limit = db.Column(Numeric(10, 2), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'corporate_customer',
    }

    def __init__(self, credit_limit: float, **kwargs):
        # corporate customer does not need max_owing
        kwargs.pop('max_owing', None)
        super().__init__(**kwargs)
        self.credit_limit = credit_limit

    def __repr__(self):
        return f"<CorporateCustomer(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, balance={self.balance}, credit_limit={self.credit_limit})>"


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

    def __init__(self, amount: float, customer_id: int):
        self.amount = amount
        self.customer_id = customer_id

    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, created_at={self.created_at}, customer_id={self.customer_id})>"


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

    def __init__(self, card_number: str, cardholder: str, expiry: str, cvv: str, **kwargs):
        super().__init__(**kwargs)
        self.card_number = card_number
        self.cardholder = cardholder
        self.expiry = expiry
        self.cvv = cvv

    def __repr__(self):
        return (f"<PayByCredit(id={self.id}, amount={self.amount}, created_at={self.created_at}, "
                f"card_number={self.card_number}, cardholder={self.cardholder}, expiry={self.expiry}, customer_id={self.customer_id})>")


class PayByDebit(Payment):
    __tablename__ = 'pay_by_debit'
    id = db.Column(db.Integer, db.ForeignKey('payment.id'), primary_key=True)
    account_number = db.Column(db.String(50), nullable=False)
    bank_name = db.Column(db.String(20), nullable=False)
    payee = db.Column(db.String(20), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'pay_by_debit',
    }

    def __init__(self, account_number: str, bank_name: str, payee: str, **kwargs):
        super().__init__(**kwargs)
        self.account_number = account_number
        self.bank_name = bank_name
        self.payee = payee

    def __repr__(self):
        return (f"<PayByDebit(id={self.id}, amount={self.amount}, created_at={self.created_at}, "
                f"account_number={self.account_number}, bank_name={self.bank_name}, payee={self.payee}, customer_id={self.customer_id})>")


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(Numeric(10, 2), nullable=False)

    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'product',
        'polymorphic_on': type,
    }

    order_items = db.relationship('OrderItem', back_populates='product')

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, type='{self.type}')>"


class Veggies(Product):
    __tablename__ = 'veggies'
    id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    pricing_unit = db.Column(
        db.Enum('per_kilo', 'per_pack', 'per_unit'), name='pricing_unit', nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'veggies',
    }

    contents = db.relationship(
        'PremadeBoxContent', back_populates='veggies', cascade='all, delete-orphan')

    def __init__(self, pricing_unit: str, **kwargs):
        super().__init__(**kwargs)
        self.pricing_unit = pricing_unit

    def __repr__(self):
        return f"<Veggies(id={self.id}, name='{self.name}', pricing_unit='{self.pricing_unit}', price={self.price})>"


class PremadeBox(Product):
    __tablename__ = 'premade_box'
    id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    box_size = db.Column(db.Enum('small', 'medium', 'large'),
                         name='premade_box_size', nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'premade_box',
    }

    contents = db.relationship(
        'PremadeBoxContent', back_populates='premade_box', cascade='all, delete-orphan')

    def __init__(self, box_size: str, **kwargs):
        super().__init__(**kwargs)
        self.box_size = box_size

    def __repr__(self):
        return f"<PremadeBox(id={self.id}, name='{self.name}', box_size='{self.box_size}', price={self.price})>"


class PremadeBoxContent(db.Model):
    __tablename__ = 'premade_box_content'

    id = db.Column(db.Integer, primary_key=True)
    premade_box_id = db.Column(db.Integer, db.ForeignKey(
        'premade_box.id'), nullable=False)
    veggies_id = db.Column(db.Integer, db.ForeignKey(
        'veggies.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)

    premade_box = db.relationship('PremadeBox', back_populates='contents')
    veggies = db.relationship('Veggies', back_populates='contents')

    def __init__(self, premade_box_id: int, veggies_id: int, quantity: float):
        self.premade_box_id = premade_box_id
        self.veggies_id = veggies_id
        self.quantity = quantity

    def __repr__(self):
        return f"<PremadeBoxContent(id={self.id}, premade_box_id={self.premade_box_id}, veggies_id={self.veggies_id}, quantity={self.quantity})>"


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    product = db.relationship('Product', back_populates='order_items')

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('Order', back_populates='order_items')

    def __init__(self, product_id: int, quantity: float, order_id: int):
        self.product_id = product_id
        self.quantity = quantity
        self.order_id = order_id

    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, order_id={self.order_id})>"


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='orders')

    order_items = db.relationship(
        'OrderItem', back_populates='order', cascade='all, delete-orphan')

    order_date = db.Column(db.Date, nullable=False, default=date.today)
    delivery_fee = db.Column(Numeric(10, 2), nullable=False, default=10.0)
    is_delivery = db.Column(db.Boolean, nullable=False, default=False)
    total_amount = db.Column(Numeric(10, 2), nullable=False, default=0.0)

    status = db.Column(db.Enum('draft', 'pending', 'processing', 'completed', 'canceled', 'refunded', name='order_status'),
                       nullable=False, default='draft')

    def __init__(self, customer_id, is_delivery=False):
        self.customer_id = customer_id
        self.is_delivery = is_delivery

    def __repr__(self):
        return f"<Order(id={self.id}, customer_id={self.customer_id}, is_delivery={self.is_delivery}, status={self.status})>"
