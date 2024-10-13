from flask import Blueprint, redirect, url_for, session
from flask import render_template
from flask import request
from fhv.dao.customer_dao import CustomerDAO
from fhv.dao.order_dao import OrderDAO
from fhv.services.customer_service import CustomerService
from fhv.exts import db

bp = Blueprint('customer', __name__, url_prefix='/customer')


@bp.route('/index')
def index():

    customer_id = session.get('user_id')
    customer_dao = CustomerDAO()
    order_dao = OrderDAO()
    customer_service = CustomerService(customer_dao, order_dao)

    draft_order_details = customer_service.get_draft_order_for_customer(
        customer_id)

    data = customer_service.get_product_list()

    return render_template('customerIndex.html',
                           data=data,
                           draft_order_details=draft_order_details)


@bp.route('/newOrder')
def newOrder():

    return redirect(url_for('customer.index'))


@bp.route('/addItemVeggie', methods=['POST'])
def addItemVeggie():
    customer_id = session.get('user_id')
    veggie_name = request.form.get('veggies')
    quantity = float(request.form.get('quantity'))

    customer_dao = CustomerDAO()
    order_dao = OrderDAO()
    customer_service = CustomerService(customer_dao, order_dao)

    customer_service.add_item_veggie(veggie_name, quantity)

    return redirect(url_for('customer.index'))
