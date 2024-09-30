from datetime import date, datetime
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
    balance = db.Column(db.Float, default=0.0)
    address = db.Column(db.String(100), nullable=True)
    max_owing = db.Column(db.Float, default=100.0)

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
    credit_limit = db.Column(db.Float, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'corporate_customer',
    }

    def __init__(self, credit_limit: float, **kwargs):
        # corporate customer do not need this attribute
        kwargs.pop('max_owing', None)
        super().__init__(**kwargs)
        self.credit_limit = credit_limit

    def __repr__(self):
        return f"<CorporateCustomer(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, balance={self.balance}>, credit_limit={self.credit_limit})"


class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'payment',
        'polymorphic_on': type,
    }

    def __init__(self, amount: float):
        self.amount = amount

    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, create_at={self.create_at})>"


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
        return (f"<PayByCredit(id={self.id}, amount={self.amount}, create_at={self.create_at}, "
                f"card_number={self.card_number}, cardholder={self.cardholder}, expiry={self.expiry})>")


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
        return (f"<PayByDebit(id={self.id}, amount={self.amount}, create_at={self.create_at}, "
                f"account_number={self.account_number}, bank_name={self.bank_name}, payee={self.payee})>")


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'product',
        'polymorphic_on': type,
    }

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


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
