from fhv.dao.customer_dao import CustomerDAO
from fhv.dao.order_dao import OrderDAO
from fhv.models import Veggies, PremadeBox, WeightedVeggie, PackVeggie, UnitVeggie


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

    def add_item_veggie(self, veggie_name, quantity):
        veggie = self.customer_dao.get_veggie_by_name(veggie_name)

        if isinstance(veggie, WeightedVeggie):
            price = veggie.price_per_kilo
            item_id = self.customer_dao.add_weighted_veggie(
                name=veggie_name, price=price, weight=quantity)

        elif isinstance(veggie, PackVeggie):
            price = veggie.price_per_pack
            item_id = self.customer_dao.add_pack_veggie(
                name=veggie_name, price=price, num_of_packs=quantity)

        elif isinstance(veggie, UnitVeggie):
            price = veggie.price_per_unit
            item_id = self.customer_dao.add_unit_veggie(
                name=veggie_name, price=price, quantity=quantity)
        return item_id

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
