from decimal import Decimal
from typing import List, Optional

from sqlalchemy import desc, extract, func
from fhv.exts import db
from sqlalchemy.orm import joinedload
from fhv.models import Payment, PremadeBox, Veggies, WeightedVeggie, PackVeggie, UnitVeggie
from sqlalchemy.orm import aliased
from sqlalchemy.orm import with_polymorphic


class StaffDAO:
    def get_daily_sales_data(self):
        result = db.session.query(
            func.date(Payment.created_at).label('date'),
            func.sum(Payment.amount).label('total_amount')
        ).group_by(func.date(Payment.created_at)).all()
        return result

    def get_weekly_sales_data(self):
        result = db.session.query(
            extract('year', Payment.created_at).label('year'),
            extract('week', Payment.created_at).label('week'),
            func.sum(Payment.amount).label('total_amount')
        ).group_by(
            extract('year', Payment.created_at),
            extract('week', Payment.created_at)
        ).order_by(
            extract('year', Payment.created_at),
            extract('week', Payment.created_at)
        ).all()
        return result

    def get_yearly_sales_data(self):
        result = db.session.query(
            extract('year', Payment.created_at).label('year'),
            func.sum(Payment.amount).label('total_amount')
        ).group_by(
            extract('year', Payment.created_at)
        ).order_by(
            extract('year', Payment.created_at)
        ).all()
        return result

    def count_most_popular_box_size(self, box_obj_list):
        box_ids = []
        for box in box_obj_list:
            box_ids.append(box.id)
        result = db.session.query(PremadeBox.box_size, func.count(PremadeBox.box_size).label('count')).filter(
            PremadeBox.id.in_(box_ids)).group_by(PremadeBox.box_size).order_by(func.count(PremadeBox.box_size).desc()).first()
        if result:
            result_dict = {"type": result[0], "count": result[1]}
        return result_dict

    def count_most_popular_weighted_veggie(self, w_veggie_obj_list):
        veggie_ids = []
        for veggie in w_veggie_obj_list:
            veggie_ids.append(veggie.id)
        result = (
            db.session.query(WeightedVeggie.name, func.sum(
                WeightedVeggie.weight).label('total_weight'))
            .filter(WeightedVeggie.id.in_(veggie_ids))
            .group_by(WeightedVeggie.name)
            .order_by(func.sum(WeightedVeggie.weight).desc())
            .first()
        )

        if result:
            return {"name": result[0], "total_weight": result[1]}
        else:
            return None

    def count_most_popular_packed_veggie(self, p_veggie_obj_list):
        veggie_ids = []
        for veggie in p_veggie_obj_list:
            veggie_ids.append(veggie.id)
        result = (
            db.session.query(PackVeggie.name, func.sum(
                PackVeggie.num_of_packs).label('total_packs'))
            .filter(PackVeggie.id.in_(veggie_ids))
            .group_by(PackVeggie.name)
            .order_by(func.sum(PackVeggie.num_of_packs).desc())
            .first()
        )

        if result:
            return {"name": result[0], "total_packs": result[1]}
        else:
            return None

    def count_most_popular_unit_veggie(self, u_veggie_obj_list):
        veggie_ids = []
        for veggie in u_veggie_obj_list:
            veggie_ids.append(veggie.id)
        result = (
            db.session.query(UnitVeggie.name, func.sum(
                UnitVeggie.quantity).label('total_units'))
            .filter(UnitVeggie.id.in_(veggie_ids))
            .group_by(UnitVeggie.name)
            .order_by(func.sum(UnitVeggie.quantity).desc())
            .first()
        )

        if result:
            return {"name": result[0], "total_units": result[1]}
        else:
            return None
