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

        # veggies
        # order1 pcustomer4
        weightedVeggie3 = WeightedVeggie(
            name="Potato(wei)", price_per_kilo=3.50, weight=1.5)

        # order2 pcustomer5
        unitVeggie3 = UnitVeggie(
            name="Broccoli(unit)", price_per_unit=2.9, quantity=3)

        # PremadeBox
        # every item = 1 kilo or 1 packs or 1 unit (any type of veggie)
        # small = 3 items
        # medium = 5 items
        # large = 8 items

        premade_box1 = PremadeBox(box_size="small", num_of_boxes=1)
        # order3 ccustomer9 small
        weightedVeggie1 = WeightedVeggie(
            name="Carrot(wei)", price_per_kilo=2.50, weight=1)
        packVeggie1 = PackVeggie(
            name="Spinach(pack)", price_per_pack=3.5, num_of_packs=2)

        premade_box2 = PremadeBox(box_size="medium", num_of_boxes=1)
        # order3 ccustomer9 medium
        weightedVeggie2 = WeightedVeggie(
            name="Tomato(wei)", price_per_kilo=5.50, weight=2)
        packVeggie2 = PackVeggie(
            name="Onion(pack)", price_per_pack=6.5, num_of_packs=3)

        premade_box3 = PremadeBox(box_size="large", num_of_boxes=1)
        # order3 ccustomer9 large 19.2 5.8 7.8
        packVeggie3 = PackVeggie(
            name="Zucchini(pack)", price_per_pack=4.8, num_of_packs=4)
        unitVeggie1 = UnitVeggie(
            name="Cucumber(unit)", price_per_unit=2.9, quantity=2)
        unitVeggie2 = UnitVeggie(
            name="Lettuce(unit)", price_per_unit=3.9, quantity=2)

        db.session.add_all([staff1, staff2, staff3,
                            customer1, customer2, customer3, customer4, customer5,
                            corporate1, corporate2, corporate3, corporate4, corporate5,
                            weightedVeggie1, weightedVeggie2, weightedVeggie3,
                            packVeggie1, packVeggie2, packVeggie3,
                            unitVeggie1, unitVeggie2, unitVeggie3,
                            premade_box1, premade_box2, premade_box3])

        db.session.flush()

        premade_box_id_1 = premade_box1.id
        premade_box_id_2 = premade_box2.id
        premade_box_id_3 = premade_box3.id

        weightedVeggie1 = weightedVeggie1.id
        packVeggie1 = packVeggie1.id

        weightedVeggie2 = weightedVeggie2.id
        packVeggie2 = packVeggie2.id

        packVeggie3 = packVeggie3.id
        unitVeggie1 = unitVeggie1.id
        unitVeggie2 = unitVeggie2.id

        order1 = Order(4, False, 5.25)
        order2 = Order(5, False, 8.7)
        order3 = Order(9, False, 72.8)

        orderItem1 = OrderItem(3, 5.25, 1)
        orderItem2 = OrderItem(9, 8.7, 2)
        orderItem3 = OrderItem(10, 9.5, 3)
        orderItem4 = OrderItem(11, 30.5, 3)
        orderItem5 = OrderItem(12, 32.8, 3)

        # PremadeBoxContent
        premade_box_content1 = PremadeBoxContent(
            premade_box_id=premade_box_id_1, veggies_id=weightedVeggie1)
        premade_box_content2 = PremadeBoxContent(
            premade_box_id=premade_box_id_1, veggies_id=packVeggie1)

        premade_box_content3 = PremadeBoxContent(
            premade_box_id=premade_box_id_2, veggies_id=weightedVeggie2)
        premade_box_content4 = PremadeBoxContent(
            premade_box_id=premade_box_id_2, veggies_id=packVeggie2)

        premade_box_content5 = PremadeBoxContent(
            premade_box_id=premade_box_id_3, veggies_id=packVeggie3)
        premade_box_content6 = PremadeBoxContent(
            premade_box_id=premade_box_id_3, veggies_id=unitVeggie1)
        premade_box_content7 = PremadeBoxContent(
            premade_box_id=premade_box_id_3, veggies_id=unitVeggie2)

        db.session.add_all([
            premade_box_content1, premade_box_content2, premade_box_content3,
            premade_box_content4, premade_box_content5, premade_box_content6, premade_box_content7,
            order1, order2, order3,
            orderItem1, orderItem2, orderItem3, orderItem4, orderItem5])

        db.session.commit()


if __name__ == "__main__":
    populate_data()
