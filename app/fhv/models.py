from datetime import date
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
    date_joined = db.Column(db.Date, nullable=False)
    department = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    def __init__(self, firstname: str, lastname: str, username: str, password: str, date_joined: date, department: str):
        super().__init__(firstname=firstname, lastname=lastname,
                         username=username, password=password)
        self.date_joined = date_joined
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

    def __init__(self, firstname: str, lastname: str, username: str, password: str, address: str = None, max_owing: float = 100.0):
        super().__init__(firstname=firstname, lastname=lastname,
                         username=username, password=password)
        self.address = address
        self.max_owing = max_owing

    def __repr__(self):
        return f"<Customer(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, balance={self.balance})>"


class CorporateCustomer(Customer):
    __tablename__ = 'corporate_customer'
    id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    credit_limit = db.Column(db.Float, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'corporate_customer',
    }

    def __init__(self, firstname: str, lastname: str, username: str, password: str, address: str, credit_limit: float):
        super().__init__(firstname, lastname, username, password, address)
        self.credit_limit = credit_limit

    def __repr__(self):
        return f"<CorporateCustomer(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, credit_limit={self.credit_limit})>"
