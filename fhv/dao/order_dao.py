from decimal import Decimal
from typing import List, Optional

from sqlalchemy import desc, func
from fhv.exts import db
from sqlalchemy.orm import joinedload
from fhv.models import Item, Veggies, PremadeBox, WeightedVeggie, PackVeggie, UnitVeggie, Order, OrderItem
from sqlalchemy.orm import aliased


class OrderDAO:
    def check_draft_order(self, customer_id):
        draft_order = Order.query.filter_by(
            customer_id=customer_id, status='draft').first()
        return draft_order

    def get_order_items_by_order_id(self, order_id):
        item_list = []

        itemLines = db.session.query(
            OrderItem.item_id,
            OrderItem.item_price,
            OrderItem.order_id,
            Item.type
        ).select_from(OrderItem).\
            outerjoin(Item, OrderItem.item_id == Item.id).\
            filter(OrderItem.order_id == order_id).all()

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
                item_detail['quantity'] = getattr(item, quantity_attr)
                if price_attr:
                    item_detail['per_price'] = getattr(item, price_attr)
                else:
                    item_detail['per_price'] = line.item_price if item_detail['quantity'] == 1 else line.item_price / \
                        item_detail['quantity']

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

    def update_order_status(self, order, status):
        order.status = status
        db.session.commit()

    def get_box_price(self, box):
        box_price = Decimal('0.00')
        for veggie in box.content:
            if isinstance(veggie, WeightedVeggie):
                box_price += veggie.price_per_kilo * veggie.weight
            elif isinstance(veggie, PackVeggie):
                box_price += veggie.price_per_pack * veggie.num_of_packs
            elif isinstance(veggie, UnitVeggie):
                box_price += veggie.price_per_unit * veggie.quantity
        return float(box_price)

    def get_type_by_item_id(self, item_id):
        item_type = db.session.query(Item.type).filter(
            Item.id == item_id).scalar()
        return item_type

    def get_order_by_id(self, order_id):
        order = Order.query.filter_by(id=order_id).first()
        return order

    def toggle_order_delivery_status(self, order):
        if order.is_delivery:
            order.is_delivery = False
        else:
            order.is_delivery = True
        db.session.commit()

    def place_draft_order(self, order):
        order.status = 'pending'
        db.session.commit()

    def get_order_list(self, customer_id: Optional[int] = None) -> List[Order]:
        query = Order.query.order_by(desc(Order.order_date))
        if customer_id is not None:
            query = query.filter_by(customer_id=customer_id)
        return query.all()

    def get_order_list_by_status(self, status):
        orders = Order.query.filter_by(
            status=status).order_by(desc(Order.order_date)).all()
        return orders if orders else None

    def count_all_type_and_content(self, all_items_id):
        results = (
            db.session.query(Item.type, func.count(Item.id).label('count'))
            .filter(Item.id.in_(all_items_id))
            .group_by(Item.type)
            .all()
        )

        result_list = []
        for type_name, count in results:
            items = (
                db.session.query(Item)
                .filter(Item.type == type_name, Item.id.in_(all_items_id))
                .all()
            )

            result_dict = {
                "type": type_name,
                "count": count,
                "content": items
            }
            result_list.append(result_dict)

        return result_list

    def get_item_ids_by_orders(self, orders):
        item_ids = []
        for order in orders:
            order_item = OrderItem.query.filter_by(order_id=order.id).first()
            item_ids.append(order_item.item_id)
        return item_ids
