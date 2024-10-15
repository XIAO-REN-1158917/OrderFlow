from fhv.exts import db
from sqlalchemy.orm import joinedload
from fhv.models import Veggies, PremadeBox, WeightedVeggie, PackVeggie, UnitVeggie, Order, OrderItem, Item


class CustomerDAO:
    def get_veggie_by_name(self, veggie_name):
        return Veggies.query.filter_by(name=veggie_name).first()

    def get_box_by_id(self, box_id):
        return db.session.query(PremadeBox).filter_by(id=box_id).first()

    def add_weighted_veggie(self, name, price, weight):
        new_item = WeightedVeggie(
            name=name, price_per_kilo=price, weight=weight)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    def add_pack_veggie(self, name, price, num_of_packs):
        new_item = PackVeggie(
            name=name, price_per_pack=price, num_of_packs=num_of_packs)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    def add_unit_veggie(self, name, price, quantity):
        new_item = UnitVeggie(
            name=name, price_per_unit=price, quantity=quantity)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    def add_premade_box(self, box_size, num_of_boxes, content):
        new_box = PremadeBox(box_size, num_of_boxes, content)
        db.session.add(new_box)
        db.session.commit()
        return new_box
