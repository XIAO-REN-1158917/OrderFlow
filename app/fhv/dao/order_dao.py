from decimal import Decimal
from fhv.exts import db
from sqlalchemy.orm import joinedload
from fhv.models import Item, PremadeBoxContent, Veggies, PremadeBox, WeightedVeggie, PackVeggie, UnitVeggie, Order, OrderItem
from sqlalchemy.orm import aliased


class OrderDAO:
    def check_draft_order(self, customer_id):
        draft_order = Order.query.filter_by(
            customer_id=customer_id, status='draft').first()
        return draft_order

    def get_draft_order_items(self, draft_order_id):
        item_list = []

        itemLines = db.session.query(
            OrderItem.item_id,
            OrderItem.item_price,
            OrderItem.order_id,
            Item.type
        ).select_from(OrderItem).\
            outerjoin(Item, OrderItem.item_id == Item.id).\
            filter(OrderItem.order_id == draft_order_id).all()

        for line in itemLines:
            item_detail = {
                'item_price': line.item_price
            }

            type_map = {
                'weighted_veggie': ('price_per_kilo', 'weight'),
                'unit_veggie': ('price_per_unit', 'quantity'),
                'pack_veggie': ('price_per_pack', 'num_of_packs'),
                'premade_box': (None, 'num_of_boxes')
            }

            item = self.get_item_detail(line.item_id)
            if line.type in type_map:
                price_attr, quantity_attr = type_map[line.type]

                item_detail['item_id'] = item.id
                item_detail['item_name'] = item.name if line.type != 'premade_box' else item.box_size

                if price_attr:
                    item_detail['per_price'] = getattr(item, price_attr)
                else:
                    item_detail['per_price'] = ''

                item_detail['quantity'] = getattr(item, quantity_attr)

            item_list.append(item_detail)

        return item_list

    def get_item_detail(self, item_id):
        result = db.session.query(Item).filter(
            Item.id == item_id).first()
        return result

    def calculate_item_price(self, price_per, quantity):
        try:
            price_per = float(price_per)
            quantity = float(quantity)

            item_price = price_per * quantity

            item_price = round(item_price, 2)

            return item_price
        except:
            return None

    def add_item_to_order(self, item_id, item_price, order_id):
        new_order_item = OrderItem(item_id, item_price, order_id)
        db.session.add(new_order_item)
        db.session.commit()

    def update_order_amount(self, order_id, price):
        order = Order.query.filter_by(id=order_id).first()
        order.order_price = order.order_price + Decimal(str(price))
        db.session.commit()
