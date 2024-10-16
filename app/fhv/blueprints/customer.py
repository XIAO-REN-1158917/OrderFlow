from flask import Blueprint, redirect, url_for, session
from flask import render_template
from flask import request
from fhv.dao.customer_dao import CustomerDAO
from fhv.dao.order_dao import OrderDAO
from fhv.dao.payment_dao import PaymentDAO

from fhv.services.customer_service import CustomerService
from fhv.exts import db

bp = Blueprint('customer', __name__, url_prefix='/customer')

# Instantiate DAO and service objects once
customer_dao = CustomerDAO()
order_dao = OrderDAO()
payment_dao = PaymentDAO()
customer_service = CustomerService(customer_dao, order_dao, payment_dao)


@bp.route('/index')
def index():
    customer_id = session.get('user_id')
    draft_order_details = customer_service.get_draft_order_for_customer(
        customer_id)
    if not draft_order_details:
        session['need_new_order'] = True
        session['order_id'] = None
    else:
        session['need_new_order'] = False
        session['order_id'] = draft_order_details['order'].id

    return render_template('customer_index.html')


@bp.route('/shoppingVeggie', methods=['GET'])
def shoppingVeggie():
    veggies = customer_service.get_veggies_list()
    return render_template('shopping_veggies.html', veggies=veggies)


@bp.route('/shoppingBox', methods=['GET'])
def shoppingBox():
    data = {
        'veggies': customer_service.get_veggies_list(),
        'premade_boxes': customer_service.get_boxes_list(),
    }
    return render_template('shopping_box.html', data=data)


@bp.route('/currentOrder', methods=['GET'])
def currentOrder():
    customer_id = session.get('user_id')
    draft_order_details = customer_service.get_draft_order_for_customer(
        customer_id)
    return render_template('current_order.html', draft_order_details=draft_order_details)


@bp.route('/newOrder')
def newOrder():
    customer_id = session.get('user_id')
    new_order = customer_service.add_new_order_for_customer(customer_id)
    print(new_order.id)
    session['order_id'] = new_order.id

    return redirect(url_for('customer.index'))


@bp.route('/addItemVeggie', methods=['POST'])
def addItemVeggie():
    customer_id = session.get('user_id')
    order_id = session.get('order_id')

    weighted_veggie = request.form.get('weighted_veggie')
    pack_veggie = request.form.get('pack_veggie')
    unit_veggie = request.form.get('unit_veggie')

    veggie_name = weighted_veggie or pack_veggie or unit_veggie
    quantity = float(request.form.get('quantity'))
    if not veggie_name:
        return redirect(url_for('customer.currentOrder'))

    print(veggie_name, quantity, order_id)
    customer_service.add_item_veggie(
        veggie_name, quantity, order_id)

    return redirect(url_for('customer.currentOrder'))


@bp.route('/addPremadeBox', methods=['POST'])
def addPremadeBox():
    order_id = session.get('order_id')
    quantity = int(request.form.get('quantity', 1))

    max_rows = 8
    selected_items = []

    for i in range(1, max_rows + 1):
        weighted_veggie = request.form.get(f'weighted_veggie_{i}')
        pack_veggie = request.form.get(f'pack_veggie_{i}')
        unit_veggie = request.form.get(f'unit_veggie_{i}')

        if weighted_veggie:
            price = customer_service.get_veggies_price(weighted_veggie)
            weighted_price = float(price)
            veggie_dict = {
                'type': 'weighted_veggie',
                'name': weighted_veggie,
                'price': weighted_price,
            }
            selected_items.append(veggie_dict)
        elif pack_veggie:
            price = customer_service.get_veggies_price(pack_veggie)
            pack_price = float(price)
            veggie_dict = {
                'type': 'pack_veggie',
                'name': pack_veggie,
                'price': pack_price,
            }
            selected_items.append(veggie_dict)
        elif unit_veggie:
            price = customer_service.get_veggies_price(unit_veggie)
            unit_price = float(price)
            veggie_dict = {
                'type': 'unit_veggie',
                'name': unit_veggie,
                'price': unit_price,
            }
            selected_items.append(veggie_dict)

    if not selected_items:
        return redirect(url_for('customer.currentOrder'))
    if len(selected_items) == 3:
        box_size = 'Small Box'
    elif len(selected_items) == 5:
        box_size = 'Medium Box'
    elif len(selected_items) == 8:
        box_size = 'Large Box'

    customer_service.add_item_box(order_id, quantity, selected_items, box_size)

    return redirect(url_for('customer.currentOrder'))


@bp.route('/removeItemFromOrder', methods=['POST'])
def removeItemFromOrder():
    item_id = request.form['item_id']
    item_price = request.form['item_price']
    order_id = session.get('order_id')
    customer_service.remove_item_form_order(order_id, item_id, item_price)
    return redirect(url_for('customer.currentOrder'))


@bp.route('/placeOrder', methods=['POST'])
def placeOrder():
    order_id = session.get('order_id')
    balance = session.get('balance')
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    customer_service.place_order(order_id, balance, user_id, user_type)
    return render_template('payment_method.html')


@bp.route('/paymentMethod')
def paymentMethod():
    order_id = session.get('order_id')
    user_id = session.get('user_id')
    can_charge_account = customer_service.can_charge_account(order_id, user_id)
    return render_template('payment_method.html', can_charge_account=can_charge_account)


@bp.route('/chargeAccount', methods=['POST'])
def chargeAccount():
    return redirect(url_for('customer.myOders'))


@bp.route('/payByCredit')
def payByCredit():
    return render_template('pay_credit.html')


@bp.route('/payByDebit')
def payByDebit():
    return render_template('pay_debit.html')


@bp.route('/toggleDelivery', methods=['POST'])
def toggleDelivery():
    order_id = session.get('order_id')
    customer_service.toggle_delivery(order_id)
    return redirect(url_for('customer.currentOrder'))


@bp.route('/myProfile/<int:user_id>')
def myProfile(user_id):
    return render_template('myProfile.html')


@bp.route('/myOrders')
def myOrders():
    return render_template('my_orders.html')
