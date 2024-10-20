from decimal import Decimal
from typing import List, Optional

from sqlalchemy import desc, extract, func
from fhv.exts import db
from sqlalchemy.orm import joinedload
from fhv.models import Payment
from sqlalchemy.orm import aliased


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
