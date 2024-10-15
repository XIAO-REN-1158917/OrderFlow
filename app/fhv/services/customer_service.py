from fhv.exts import db
from fhv.dao.customer_dao import CustomerDAO
from fhv.dao.order_dao import OrderDAO
from fhv.models import Veggies, PremadeBox, WeightedVeggie, PackVeggie, UnitVeggie, Order, Item


class CustomerService:
    def __init__(self, customer_dao: CustomerDAO, order_dao: OrderDAO):
        self.customer_dao = customer_dao
        self.order_dao = order_dao

    def get_veggies_list(self):
        veggies = [
            {
                'name': 'Carrot(wei)',
                'price': 2.50,
                'unit': '/Kg',
                'type': 'weighted_veggie'
            },
            {
                'name': 'Tomato(wei)',
                'price': 5.50,
                'unit': '/Kg',
                'type': 'weighted_veggie'
            },
            {
                'name': 'Potato(wei)',
                'price': 3.50,
                'unit': '/Kg',
                'type': 'weighted_veggie'
            },
            {
                'name': 'Spinach(pack)',
                'price': 3.50,
                'unit': '/Pack',
                'type': 'pack_veggie'
            },
            {
                'name': 'Onion(pack)',
                'price': 6.50,
                'unit': '/Pack',
                'type': 'pack_veggie'
            },
            {
                'name': 'Zucchini(pack)',
                'price': 4.80,
                'unit': '/Pack',
                'type': 'pack_veggie'
            },
            {
                'name': 'Cucumber(unit)',
                'price': 2.90,
                'unit': '/Unit',
                'type': 'unit_veggie'
            },
            {
                'name': 'Lettuce(unit)',
                'price': 3.90,
                'unit': '/Unit',
                'type': 'unit_veggie'
            },
            {
                'name': 'Broccoli(unit)',
                'price': 2.90,
                'unit': '/Unit',
                'type': 'unit_veggie'
            },
        ]
        return veggies

    def get_veggies_price(self, name: str):
        veggies = self.get_veggies_list()
        for veggie in veggies:
            if veggie['name'] == name:
                return veggie['price']
        return None

    def get_boxes_list(self):
        premade_boxes = [
            {'name': 'Small Box', 'capacity': 3},
            {'name': 'Medium Box', 'capacity': 5},
            {'name': 'Large Box', 'capacity': 8},
        ]
        return premade_boxes

    def add_item_veggie(self, veggie_name, quantity, order_id):
        veggie = self.customer_dao.get_veggie_by_name(veggie_name)

        veggie_type_map = {
            WeightedVeggie: ('price_per_kilo', 'weight', 'add_weighted_veggie'),
            PackVeggie: ('price_per_pack', 'num_of_packs', 'add_pack_veggie'),
            UnitVeggie: ('price_per_unit', 'quantity', 'add_unit_veggie')
        }

        for veggie_type, (price_attr, quantity_attr, add_method_name) in veggie_type_map.items():
            if isinstance(veggie, veggie_type):
                price = getattr(veggie, price_attr)
                item_price = self.order_dao.calculate_item_price(
                    price, quantity)
                add_method = getattr(self.customer_dao, add_method_name)
                item_id = add_method(
                    name=veggie_name, price=price, **{quantity_attr: quantity})
                item_id = item_id.id

                self.order_dao.add_item_to_order(item_id, item_price, order_id)
                self.order_dao.update_order_amount(order_id, item_price)

                return item_id, item_price

        return None, None

    def add_item_box(self, order_id, quantity, selected_items):
        content = []
        for item in selected_items:
            if item['type'] == 'weighted_veggie':
                veggie_in_box = self.customer_dao.add_weighted_veggie(
                    item['name'], item['price'], 1)
            elif item['type'] == 'pack_veggie':
                veggie_in_box = self.customer_dao.add_pack_veggie(
                    item['name'], item['price'], 1)
            elif item['type'] == 'unit_veggie':
                veggie_in_box = self.customer_dao.add_unit_veggie(
                    item['name'], item['price'], 1)
            content.append(veggie_in_box)
        if len(content) == 3:
            box_size = 'Small Box'
        elif len(content) == 5:
            box_size = 'Medium Box'
        elif len(content) == 8:
            box_size = 'Large Box'
        new_box = self.customer_dao.add_premade_box(
            box_size, quantity, content)
        box_price = self.order_dao.get_box_price(new_box)
        self.order_dao.add_item_to_order(new_box.id, box_price, order_id)
        item_price = box_price*quantity
        self.order_dao.update_order_amount(order_id, item_price)

    def get_draft_order_for_customer(self, customer_id):
        draft_order_details = {}
        draft_order = self.order_dao.check_draft_order(customer_id)
        if draft_order:

            items = self.order_dao.get_draft_order_items(draft_order.id)
            draft_order_details = {
                'order': draft_order,
                'items': items
            }
        else:
            draft_order_details = None
        return draft_order_details

    def add_new_order_for_customer(self, customer_id):
        order = Order(customer_id)
        db.session.add(order)
        db.session.commit()
        return order

    def remove_item_form_order(self, order_id, item_id, item_price):
        item_type = self.order_dao.get_type_by_item_id(item_id)
        if item_type == 'premade_box':
            box = self.customer_dao.get_box_by_id(item_id)
            for veggie in box.content:
                item_to_delete = Item.query.get(veggie.id)
                db.session.delete(item_to_delete)
                db.session.commit()

        item_to_delete = Item.query.get(item_id)
        db.session.delete(item_to_delete)
        db.session.commit()
        item_price = round(-float(item_price), 2)
        self.order_dao.update_order_amount(order_id, item_price)
