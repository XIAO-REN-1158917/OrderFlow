'''
Run the following command in the app directory
python -m scripts.populate_db
'''
from datetime import date
from fhv import create_app, db
from fhv.models import Person, Staff, Customer, CorporateCustomer, Product, Veggies, PremadeBox, PremadeBoxContent

app = create_app()


def populate_data():
    with app.app_context():
        # staff
        staff1 = Staff(firstname='John', lastname='Doe',
                       username='johndoe', password='john123', department='Sales')
        staff2 = Staff(firstname='Jane', lastname='Smith',
                       username='janesmith', password='jane123', department='Marketing')
        staff3 = Staff(firstname='Alice', lastname='Johnson',
                       username='alicejohnson', password='alice123', department='IT')
        # private customer
        customer1 = Customer(firstname='Bob', lastname='Brown',
                             username='bobbrown', password='bob123', address='Riccarton Chch')
        customer2 = Customer(firstname='Charlie', lastname='Taylor',
                             username='charlietaylor', password='charlie123', address='Addington Chch')
        customer3 = Customer(firstname='David', lastname='Walker',
                             username='davidwalker', password='david123', address='Merivale Chch')
        customer4 = Customer(firstname='Eva', lastname='Clark',
                             username='evaclark', password='eva123', address='Halswell Chch')
        customer5 = Customer(firstname='Frank', lastname='Wright',
                             username='frankwright', password='frank123', address='Hornby Chch')
        customer6 = Customer(firstname='Grace', lastname='Lee',
                             username='gracelee', password='grace123', address='Ilam Chch')
        customer7 = Customer(firstname='Henry', lastname='Scott',
                             username='henryscott', password='henry123', address='Riccarton Chch')
        customer8 = Customer(firstname='Isaac', lastname='Wright',
                             username='isaacwright', password='isaac123', address='Addington Chch')
        customer9 = Customer(firstname='Jack', lastname='Taylor',
                             username='jacktaylor', password='jack123', address='Merivale Chch')
        customer10 = Customer(firstname='Kelly', lastname='Johnson',
                              username='kellyjohnson', password='kelly123', address='Halswell Chch')
        # corporate customer
        corporate1 = CorporateCustomer(firstname='Liam', lastname='Brown',
                                       username='liambrown', password='liam123', address='Riccarton Chch', credit_limit=2000.0)
        corporate2 = CorporateCustomer(firstname='Mia', lastname='Taylor',
                                       username='miataylor', password='mia123', address='Addington Chch', credit_limit=3000.0)
        corporate3 = CorporateCustomer(firstname='Noah', lastname='Walker',
                                       username='noahwalker', password='noah123', address='Merivale Chch', credit_limit=4000.0)
        corporate4 = CorporateCustomer(firstname='Olivia', lastname='Clark',
                                       username='oliviaclark', password='olivia123', address='Halswell Chch', credit_limit=5000.0)
        corporate5 = CorporateCustomer(firstname='Paul', lastname='Wright',
                                       username='paulwright', password='paul123', address='Hornby Chch', credit_limit=2500.0)
        corporate6 = CorporateCustomer(firstname='Quincy', lastname='Lee',
                                       username='quincylee', password='quincy123', address='Ilam Chch', credit_limit=3500.0)
        corporate7 = CorporateCustomer(firstname='Rachel', lastname='Scott',
                                       username='rachelscott', password='rachel123', address='Riccarton Chch', credit_limit=4500.0)
        corporate8 = CorporateCustomer(firstname='Sam', lastname='Wright',
                                       username='samwright', password='sam123', address='Addington Chch', credit_limit=1500.0)
        corporate9 = CorporateCustomer(firstname='Tina', lastname='Taylor',
                                       username='tinataylor', password='tina123', address='Merivale Chch', credit_limit=3000.0)
        corporate10 = CorporateCustomer(firstname='Uma', lastname='Johnson',
                                        username='umajohnson', password='uma123', address='Halswell Chch', credit_limit=1000.0)
        # veggies
        veggies1 = Veggies(name="Carrot", price=2.50, pricing_unit="per_kilo")
        veggies2 = Veggies(name="Tomato", price=3.00, pricing_unit="per_pack")
        veggies3 = Veggies(name="Cucumber", price=1.50,
                           pricing_unit="per_unit")
        veggies4 = Veggies(name="Spinach", price=4.00, pricing_unit="per_kilo")
        veggies5 = Veggies(name="Potato", price=1.20, pricing_unit="per_kilo")
        veggies6 = Veggies(name="Lettuce", price=1.00, pricing_unit="per_pack")
        veggies7 = Veggies(name="Broccoli", price=2.80,
                           pricing_unit="per_unit")
        veggies8 = Veggies(name="Cauliflower", price=3.20,
                           pricing_unit="per_unit")
        veggies9 = Veggies(name="Zucchini", price=2.00,
                           pricing_unit="per_kilo")
        veggies10 = Veggies(name="Onion", price=1.50, pricing_unit="per_kilo")

        # PremadeBox
        premade_box1 = PremadeBox(name="Box 1", price=20.00, box_size="small")
        premade_box2 = PremadeBox(name="Box 2", price=25.00, box_size="medium")
        premade_box3 = PremadeBox(name="Box 3", price=30.00, box_size="large")
        premade_box4 = PremadeBox(name="Box 4", price=35.00, box_size="medium")
        premade_box5 = PremadeBox(name="Box 5", price=40.00, box_size="large")

        db.session.add_all([staff1, staff2, staff3,
                            customer1, customer2, customer3, customer4, customer5,
                            customer6, customer7, customer8, customer9, customer10, corporate1, corporate2, corporate3,
                            corporate4, corporate5, corporate6, corporate7, corporate8, corporate9, corporate10,
                            veggies1, veggies2, veggies3, veggies4, veggies5,
                            veggies6, veggies7, veggies8, veggies9, veggies10,
                            premade_box1, premade_box2, premade_box3, premade_box4, premade_box5])

        db.session.flush()

        premade_box_id_1 = premade_box1.id
        premade_box_id_2 = premade_box2.id
        veggies_id_1 = veggies1.id
        veggies_id_2 = veggies2.id

        # PremadeBoxContent
        premade_box_content1 = PremadeBoxContent(
            premade_box_id=premade_box_id_1, veggies_id=veggies_id_1, quantity=2.0)
        premade_box_content2 = PremadeBoxContent(
            premade_box_id=premade_box_id_1, veggies_id=veggies_id_2, quantity=3.0)
        premade_box_content3 = PremadeBoxContent(
            premade_box_id=premade_box_id_2, veggies_id=veggies_id_1, quantity=1.0)
        premade_box_content4 = PremadeBoxContent(
            premade_box_id=premade_box_id_2, veggies_id=veggies_id_2, quantity=2.5)

        db.session.add_all([
            premade_box_content1, premade_box_content2, premade_box_content3,
            premade_box_content4])

        db.session.commit()


if __name__ == "__main__":
    populate_data()
