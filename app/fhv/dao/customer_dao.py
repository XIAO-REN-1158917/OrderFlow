from fhv.exts import db
from sqlalchemy.orm import joinedload
from fhv.models import Veggies, PremadeBox, WeightedVeggie, PackVeggie, UnitVeggie, Order, OrderItem


class CustomerDAO:
    def get_all_veggies(self):
        veggies = Veggies.query.distinct(Veggies.name).all()
        veggie_list = []
        for veggie in veggies:
            if isinstance(veggie, WeightedVeggie):
                price = veggie.price_per_kilo
                unit = '/Kg'
            elif isinstance(veggie, PackVeggie):
                price = veggie.price_per_pack
                unit = '/Pack'
            elif isinstance(veggie, UnitVeggie):
                price = veggie.price_per_unit
                unit = '/Unit'
            else:
                price = None

            veggie_list.append({
                'id': veggie.id,
                'name': veggie.name,
                'price': price,
                'unit': unit
            })
        return veggie_list

    def get_veggie_by_name(self, veggie_name):
        return Veggies.query.filter_by(name=veggie_name).first()

    def add_weighted_veggie(self, name, price, weight):
        new_item = WeightedVeggie(
            name=name, price_per_kilo=price, weight=weight)
        db.session.add(new_item)
        db.session.commit()
        return new_item.id

    def add_pack_veggie(self, name, price, num_of_packs):
        new_item = PackVeggie(
            name=name, price_per_pack=price, num_of_packs=num_of_packs)
        db.session.add(new_item)
        db.session.commit()
        return new_item.id

    def add_unit_veggie(self, name, price, quantity):
        new_item = UnitVeggie(
            name=name, price_per_unit=price, quantity=quantity)
        db.session.add(new_item)
        db.session.commit()
        return new_item.id

    def check_draft_order_by_customer_id(self, customer_id):
        draft_order = Order.query.filter_by(
            customer_id=customer_id, status='draft').first()
        return draft_order

    def get_veggie_with_details(self, veggie_id):
        veggie = Veggies.query.options(
            joinedload(Veggies.weightedveggie),
            joinedload(Veggies.packveggie),
            joinedload(Veggies.unitveggie)
        ).filter_by(id=veggie_id).first()
