from fhv.exts import db
from fhv.dao.customer_dao import CustomerDAO
from fhv.dao.order_dao import OrderDAO
from fhv.dao.payment_dao import PaymentDAO
from fhv.dao.staff_dao import StaffDAO

from fhv.models import Order, Item, Customer


class StaffService:
    def __init__(self, customer_dao: CustomerDAO, order_dao: OrderDAO, payment_dao: PaymentDAO, staff_dao: StaffDAO):
        self.customer_dao = customer_dao
        self.order_dao = order_dao
        self.payment_dao = payment_dao
        self.staff_dao = staff_dao

    def get_all_orders(self, stauts):
        return self.order_dao.get_order_list_by_status(stauts)

    def get_customer(self, customer_id):
        return self.customer_dao.get_customer_by_id(customer_id)

    def get_all_customer(self):
        return self.customer_dao.all_customer('staff')

    def fulfill_order(self, order_id):
        order = self.order_dao.get_order_by_id(order_id)
        self.order_dao.update_order_status(order, 'fulfilled')

    def get_daily_sales(self):
        result = self.staff_dao.get_daily_sales_data()
        daily = [
            {'date': row.date, 'total_amount': row.total_amount} for row in result]
        return daily

    def get_weekly_sales(self):
        result = self.staff_dao.get_weekly_sales_data()
        weekly = [
            {'date': f"{
                row.year}-W{int(row.week):02}", 'total_amount': row.total_amount}
            for row in result
        ]
        return weekly

    def get_yearly_sales(self):
        result = self.staff_dao.get_yearly_sales_data()
        yearly = [
            {'date': int(row.year), 'total_amount': row.total_amount} for row in result]
        return yearly
