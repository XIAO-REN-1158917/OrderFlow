from fhv.exts import db
from fhv.dao.customer_dao import CustomerDAO
from fhv.dao.order_dao import OrderDAO
from fhv.models import Veggies, PremadeBox, WeightedVeggie, PackVeggie, UnitVeggie, Order


class CustomerService:
    def __init__(self, customer_dao: CustomerDAO, order_dao: OrderDAO):
        self.customer_dao = customer_dao
        self.order_dao = order_dao

    def get_product_list(self):
        veggies = self.customer_dao.get_all_veggies()
        premade_boxes = [
            {'name': 'Small Box', 'capacity': 3},
            {'name': 'Medium Box', 'capacity': 5},
            {'name': 'Large Box', 'capacity': 8},
        ]
        return {
            'veggies': veggies,
            'premade_boxes': premade_boxes,
        }

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

                self.order_dao.add_item_to_order(item_id, item_price, order_id)
                self.order_dao.update_order_amount(order_id, item_price)

                return item_id, item_price

        return None, None

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
