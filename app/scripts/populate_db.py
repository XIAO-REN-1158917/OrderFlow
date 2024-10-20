'''
Run the following command in the app directory
python -m scripts.populate_db
'''
from datetime import date
from fhv import create_app, db
from fhv.models import *

app = create_app()


def populate_data():
    with app.app_context():
        # staff
        staff1 = Staff(firstname='John', lastname='Jod',
                       username='staff1', password='staff123', department='SalesA')
        staff2 = Staff(firstname='Jane', lastname='Marry',
                       username='staff2', password='staff123', department='SalesB')
        staff3 = Staff(firstname='Alice', lastname='Smith',
                       username='staff3', password='staff123', department='SalesC')
        # private customer
        customer1 = Customer(firstname='Bob', lastname='James',
                             username='pcustomer4', password='pcustomer123', address='Riccarton Chch')
        customer2 = Customer(firstname='Charlie', lastname='Taylor',
                             username='pcustomer5', password='pcustomer123', address='Addington Chch')
        customer3 = Customer(firstname='David', lastname='Walker',
                             username='pcustomer6', password='pcustomer123', address='Merivale Chch')
        customer4 = Customer(firstname='Eva', lastname='Clark',
                             username='pcustomer7', password='pcustomer123', address='Halswell Chch')
        customer5 = Customer(firstname='Frank', lastname='Wright',
                             username='pcustomer8', password='pcustomer123', address='Hornby Chch')
        # corporate customer
        corporate1 = CorporateCustomer(firstname='Liam', lastname='Brown',
                                       username='ccustomer9', password='ccustomer123', address='Riccarton Chch', credit_limit=2000.0)
        corporate2 = CorporateCustomer(firstname='Mia', lastname='Taylor',
                                       username='ccustomer10', password='ccustomer123', address='Addington Chch', credit_limit=3000.0)
        corporate3 = CorporateCustomer(firstname='Noah', lastname='Walker',
                                       username='ccustomer11', password='ccustomer123', address='Merivale Chch', credit_limit=4000.0)
        corporate4 = CorporateCustomer(firstname='Olivia', lastname='Clark',
                                       username='ccustomer12', password='ccustomer123', address='Halswell Chch', credit_limit=5000.0)
        corporate5 = CorporateCustomer(firstname='Paul', lastname='Wright',
                                       username='ccustomer13', password='ccustomer123', address='Hornby Chch', credit_limit=6000.0)

        db.session.add_all([staff1, staff2, staff3,
                            customer1, customer2, customer3, customer4, customer5,
                            corporate1, corporate2, corporate3, corporate4, corporate5,
                            ])

        db.session.commit()


if __name__ == "__main__":
    populate_data()
