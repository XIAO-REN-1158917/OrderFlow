'''
Here are the business requirements for the customer.
'''
from fhv.exts import db
from fhv.dao.customer_dao import CustomerDAO
from fhv.dao.order_dao import OrderDAO
from fhv.dao.payment_dao import PaymentDAO

from fhv.models import Order, Item, Customer


class CustomerService:
    def __init__(self, customer_dao: CustomerDAO, order_dao: OrderDAO, payment_dao: PaymentDAO):
        self.customer_dao = customer_dao
        self.order_dao = order_dao
        self.payment_dao = payment_dao

    def get_veggies_list(self):
        """
        This is just static data. I didn't store the static data in the database 
        because this project focuses more on order processing. 
        Additionally, there is no need for any editing of the static product data.
        """
        veggies = [
            {
                'name': 'Carrot(wei)',
                'price': 2.50,
                'unit': '/Kg',
                'type': 'weighted_veggie'
            },
            {
                'name': 'Tomato(wei)',
                'price': 5.50,
                'unit': '/Kg',
                'type': 'weighted_veggie'
            },
            {
                'name': 'Potato(wei)',
                'price': 3.50,
                'unit': '/Kg',
                'type': 'weighted_veggie'
            },
            {
                'name': 'Spinach(pack)',
                'price': 3.50,
                'unit': '/Pack',
                'type': 'pack_veggie'
            },
            {
                'name': 'Onion(pack)',
                'price': 6.50,
                'unit': '/Pack',
                'type': 'pack_veggie'
            },
            {
                'name': 'Zucchini(pack)',
                'price': 4.80,
                'unit': '/Pack',
                'type': 'pack_veggie'
            },
            {
                'name': 'Cucumber(unit)',
                'price': 2.90,
                'unit': '/Unit',
                'type': 'unit_veggie'
            },
            {
                'name': 'Lettuce(unit)',
                'price': 3.90,
                'unit': '/Unit',
                'type': 'unit_veggie'
            },
            {
                'name': 'Broccoli(unit)',
                'price': 2.90,
                'unit': '/Unit',
                'type': 'unit_veggie'
            },
        ]
        return veggies

    def get_veggies_price(self, name: str):
        veggies = self.get_veggies_list()
        for veggie in veggies:
            if veggie['name'] == name:
                return veggie['price']
        return None

    def get_veggies_type(self, name):
        veggies = self.get_veggies_list()
        for veggie in veggies:
            if veggie['name'] == name:
                return veggie['type']

    def get_boxes_list(self):
        '''
        This is just static data, documenting my definitions for the premade boxes.
        '''
        premade_boxes = [
            {'name': 'Small Box', 'capacity': 3},
            {'name': 'Medium Box', 'capacity': 5},
            {'name': 'Large Box', 'capacity': 8},
        ]
        return premade_boxes

    def add_item_veggie(self, veggie_name, quantity, order_id):
        veggie = self.get_veggies_type(veggie_name)
        price = self.get_veggies_price(veggie_name)
        if veggie == 'weighted_veggie':
            item = self.customer_dao.add_weighted_veggie(
                veggie_name, price, quantity)
        elif veggie == 'pack_veggie':
            item = self.customer_dao.add_pack_veggie(
                veggie_name, price, quantity)
        elif veggie == 'unit_veggie':
            item = self.customer_dao.add_unit_veggie(
                veggie_name, price, quantity)
        item_price = self.order_dao.calculate_item_price(price, quantity)
        self.order_dao.add_item_to_order(item.id, item_price, order_id)
        self.order_dao.update_order_amount(order_id, item_price)

    def add_item_box(self, order_id, quantity, selected_items, box_size):
        new_box = self.customer_dao.add_premade_box(
            box_size, quantity, None)
        for item in selected_items:
            if item['type'] == 'weighted_veggie':
                veggie_in_box = self.customer_dao.add_weighted_veggie(
                    item['name'], item['price'], 1)
            elif item['type'] == 'pack_veggie':
                veggie_in_box = self.customer_dao.add_pack_veggie(
                    item['name'], item['price'], 1)
            elif item['type'] == 'unit_veggie':
                veggie_in_box = self.customer_dao.add_unit_veggie(
                    item['name'], item['price'], 1)
            new_box.content.append(veggie_in_box)

        box_price = self.order_dao.get_box_price(new_box)
        item_price = self.order_dao.calculate_item_price(box_price, quantity)
        self.order_dao.add_item_to_order(new_box.id, item_price, order_id)
        self.order_dao.update_order_amount(order_id, item_price)

    def get_draft_order_for_customer(self, customer_id):
        draft_order_details = {}
        draft_order = self.order_dao.check_draft_order(customer_id)
        if draft_order:
            items = self.order_dao.get_order_items_by_order_id(draft_order.id)
            draft_order_details = {
                'order': draft_order,  # order info
                'items': items  # order items info
            }
        else:
            draft_order_details = None
        return draft_order_details

    def add_new_order_for_customer(self, customer_id):
        order = Order(customer_id)
        db.session.add(order)
        db.session.commit()
        return order

    def remove_item_form_order(self, order_id, item_id, item_price):
        item_to_delete = Item.query.get(item_id)
        db.session.delete(item_to_delete)
        db.session.commit()
        item_price = round(-float(item_price), 2)
        self.order_dao.update_order_amount(order_id, item_price)

    def toggle_delivery(self, order_id):
        order = self.order_dao.get_order_by_id(order_id)
        price = order.delivery_fee
        if order.is_delivery:
            price = round(-float(price), 2)
        self.order_dao.update_order_amount(order_id, price)
        self.order_dao.toggle_order_delivery_status(order)

    def can_charge_account(self, order_id, user_id):
        order = self.order_dao.get_order_by_id(order_id)
        user = self.customer_dao.get_user_by_id(user_id)
        if isinstance(user, Customer):
            return order.order_price+user.balance <= user.max_owing, order.order_price
        else:
            return order.order_price+user.balance <= user.credit_limit, order.order_price

    def charge_account(self, order_id, user_id):
        order = self.order_dao.get_order_by_id(order_id)
        user = self.customer_dao.get_user_by_id(user_id)
        self.payment_dao.update_balance(order.order_price, user)
        self.order_dao.update_order_status(order, 'pending')

    def get_all_orders_for_customer(self, customer_id):
        orders = self.order_dao.get_order_list(customer_id)
        return orders

    def get_order_detail_by_order_id(self, order_id):
        orderDetail = {}
        orderInfo = self.order_dao.get_order_by_id(order_id)
        if orderInfo:
            items = self.order_dao.get_order_items_by_order_id(orderInfo.id)
            orderDetail = {
                'order': orderInfo,
                'items': items
            }
        else:
            orderDetail = None
        return orderDetail

    def cancel_pending_order_charge_account(self, order_id, user_id):
        order = self.order_dao.get_order_by_id(order_id)
        user = self.customer_dao.get_user_by_id(user_id)
        self.order_dao.update_order_status(order, 'canceled')
        subtraction = -order.order_price
        self.payment_dao.update_balance(subtraction, user)

    def processing_pay_by_credit_order(self, order_id, card_number, cardholder, expiry, cvv):
        order = self.order_dao.get_order_by_id(order_id)
        self.order_dao.update_order_status(order, 'pending')
        self.payment_dao.add_new_payment_credit(
            order.order_price, order.customer_id, card_number, cardholder, expiry, cvv)

    def processing_pay_by_credit_balance(self, user_id, order_amount, card_number, cardholder, expiry, cvv):
        user = self.customer_dao.get_user_by_id(user_id)
        subtraction = -float(order_amount)
        self.payment_dao.update_balance(subtraction, user)
        self.payment_dao.add_new_payment_credit(
            order_amount, user.id, card_number, cardholder, expiry, cvv)

    def processing_pay_by_debit_order(self, order_id, account_number, bank_name, payee):
        order = self.order_dao.get_order_by_id(order_id)
        self.order_dao.update_order_status(order, 'pending')
        self.payment_dao.add_new_payment_debit(
            order.order_price, order.customer_id, account_number, bank_name, payee)

    def processing_pay_by_debit_balance(self, user_id, order_amount, account_number, bank_name, payee):
        user = self.customer_dao.get_user_by_id(user_id)
        subtraction = -float(order_amount)
        self.payment_dao.update_balance(subtraction, user)
        self.payment_dao.add_new_payment_debit(
            order_amount, user.id, account_number, bank_name, payee)

    def get_payments_for_customer(self, user_id):
        return self.payment_dao.get_payment_list(user_id)
