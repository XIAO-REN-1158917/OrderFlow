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
            item_detail = {}
            item_detail['item_price'] = line.item_price

            if line.type == 'weighted_veggie':
                wei_veggie = self.get_item_detail_veggie(line.item_id)
                item_detail['item_id'] = wei_veggie.id
                item_detail['item_name'] = wei_veggie.name
                item_detail['per_price'] = wei_veggie.price_per_kilo
                item_detail['quantity'] = wei_veggie.weight

            elif line.type == 'unit_veggie':
                unit_veggie = self.get_item_detail_veggie(line.item_id)
                item_detail['item_id'] = unit_veggie.id
                item_detail['item_name'] = unit_veggie.name
                item_detail['per_price'] = unit_veggie.price_per_unit
                item_detail['quantity'] = unit_veggie.quantity

            elif line.type == 'pack_veggie':
                pack_veggie = self.get_item_detail_veggie(line.item_id)
                item_detail['item_id'] = pack_veggie.id
                item_detail['item_name'] = pack_veggie.name
                item_detail['per_price'] = pack_veggie.price_per_pack
                item_detail['quantity'] = pack_veggie.num_of_packs

            elif line.type == 'premade_box':
                box = self.get_item_detail_premade_box(line.item_id)
                item_detail['item_id'] = box.id
                item_detail['item_name'] = box.box_size
                item_detail['per_price'] = ''
                item_detail['quantity'] = box.num_of_boxes

            item_list.append(item_detail)

        return item_list

    def get_item_detail_veggie(self, veggie_id):
        result = db.session.query(Veggies).filter(
            Veggies.id == veggie_id).first()
        return result

    def get_item_detail_premade_box(self, premade_box_id):
        result = db.session.query(Item).filter(
            Item.id == premade_box_id).first()

        return result
