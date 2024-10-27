'''
Here are the business requirements for the staff.
'''
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
            {'date': f"{row.year}-W{int(row.week):02}",
             'total_amount': row.total_amount}
            for row in result
        ]
        return weekly

    def get_yearly_sales(self):
        result = self.staff_dao.get_yearly_sales_data()
        yearly = [
            {'date': int(row.year), 'total_amount': row.total_amount} for row in result]
        return yearly

    def top_item(self):
        """
        There are four types of products, each displaying the top-selling item. 
        If it's a premade box, the most popular size is shown. 
        For vegetables, the total sales are calculated by summing their quantities(kilo or packs or unit), 
        identifying the one with the highest cumulative sales.
        """
        box_result = None
        weighted_veggie_result = None
        packed_veggie_result = None
        unit_veggie_result = None
        orders = self.order_dao.get_order_list_by_status('fulfilled')
        item_id_list = self.order_dao.get_item_ids_by_orders(orders)
        result = self.order_dao.count_all_type_and_content(item_id_list)
        for r in result:
            if r['type'] == 'premade_box':
                box_result = self.staff_dao.count_most_popular_box_size(
                    r['content'])
            elif r['type'] == 'weighted_veggie':
                weighted_veggie_result = self.staff_dao.count_most_popular_weighted_veggie(
                    r['content'])
            elif r['type'] == 'pack_veggie':
                packed_veggie_result = self.staff_dao.count_most_popular_packed_veggie(
                    r['content'])
            elif r['type'] == 'unit_veggie':
                unit_veggie_result = self.staff_dao.count_most_popular_unit_veggie(
                    r['content'])
        return box_result, weighted_veggie_result, packed_veggie_result, unit_veggie_result
