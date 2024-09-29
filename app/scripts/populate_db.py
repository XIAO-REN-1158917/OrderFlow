'''
Run the following command in the app directory
python -m scripts.populate_db
'''
from datetime import date
from fhv import create_app, db
from fhv.models import Person, Staff, Customer, CorporateCustomer

app = create_app()


def populate_data():
    with app.app_context():

        person1 = Person(firstname='per', lastname='son',
                         username='person', password='person123')
        staff1 = Staff(firstname='sta', lastname='ff',
                       username='staff', password='staff123', date_joined=date.today(), department='departmentA')
        customer1 = Customer(firstname='cust', lastname='mer',
                             username='customer', password='customer123', address='Riccarton Chch')
        corporate1 = CorporateCustomer(firstname='corpo', lastname='rate',
                                       username='corporate', password='corporate123', address='Riccarton Chch', credit_limit=1000.0)

        db.session.add_all([person1, staff1, customer1, corporate1])

        db.session.commit()


if __name__ == "__main__":
    populate_data()
