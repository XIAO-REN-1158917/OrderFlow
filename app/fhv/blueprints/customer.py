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
    customer_id = session.get('user_id')
    customer_dao = CustomerDAO()
    order_dao = OrderDAO()
    customer_service = CustomerService(customer_dao, order_dao)
    new_order = customer_service.add_new_order_for_customer(customer_id)
    print(new_order.id)
    session['order_id'] = new_order.id

    return redirect(url_for('customer.index'))


@bp.route('/addItemVeggie', methods=['POST'])
def addItemVeggie():
    customer_id = session.get('user_id')
    order_id = session.get('order_id')
    veggie_name = request.form.get('veggies')
    quantity = float(request.form.get('quantity'))

    customer_dao = CustomerDAO()
    order_dao = OrderDAO()
    customer_service = CustomerService(customer_dao, order_dao)

    customer_service.add_item_veggie(
        veggie_name, quantity, order_id)

    return redirect(url_for('customer.index'))


@bp.route('/addPremadeBox', methods=['POST'])
def addPremadeBox():
    premade_box_name = request.form.get('premade_box')
    box_quantity = request.form['box_quantity']
    print(box_quantity)
    if not premade_box_name:
        print(1)
        return redirect(url_for('customer.index'))

    veggie_options = []

    for i in range(1, 9):
        veggie_option = request.form.get(f'veggie-option-{i}')
        if veggie_option:
            print(veggie_option)
            veggie_options.append(veggie_option)

    if len(veggie_options) < 3:
        print(2)
        return redirect(url_for('customer.index'))

    return redirect(url_for('customer.index'))
