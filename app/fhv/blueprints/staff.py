from flask import Blueprint, redirect, url_for, session
from flask import render_template
from flask import request
from fhv.dao.customer_dao import CustomerDAO
from fhv.dao.order_dao import OrderDAO
from fhv.dao.payment_dao import PaymentDAO

from fhv.services.customer_service import CustomerService
from fhv.services.staff_service import StaffService

bp = Blueprint('staff', __name__, url_prefix='/staff')

customer_dao = CustomerDAO()
order_dao = OrderDAO()
payment_dao = PaymentDAO()

staff_service = StaffService(customer_dao, order_dao, payment_dao)
customer_service = CustomerService(customer_dao, order_dao, payment_dao)


@bp.route('/index')
def index():
    return render_template('staffIndex.html')


@bp.route('/currentOrdersForStaff')
def currentOrdersForStaff():
    currentOrders = staff_service.get_all_orders('pending')
    return render_template('current_orders_staff.html', currentOrders=currentOrders)


@bp.route('/previousOdersForStaff')
def previousOdersForStaff():
    previousOders = staff_service.get_all_orders('fulfilled')
    return render_template('privous_order_staff.html', previousOders=previousOders)


@bp.route('/workOnPendingOrder/<int:order_id>')
def workOnPendingOrder(order_id):
    orderDetail = customer_service.get_order_detail_by_order_id(order_id)
    customer_id = orderDetail['order'].customer_id
    customer = staff_service.get_customer(customer_id)
    return render_template('staff_work_on_order.html',
                           orderDetail=orderDetail,
                           customer=customer)


@bp.route('/fulfillOrder', methods=['POST'])
def fulfillOrder():
    order_id = request.form['order_id']
    staff_service.fulfill_order(order_id)
    return redirect('currentOrdersForStaff')


@bp.route('/customerList')
def customerList():
    customers = staff_service.get_all_customer()
    return render_template('customer_list.html', customers=customers)


@bp.route('/customerDetails/<int:customer_id>')
def customerDetails(customer_id):
    customer = staff_service.get_customer(customer_id)
    orders = customer_service.get_all_orders_for_customer(customer_id)
    payments = customer_service.get_payments_for_customer(customer_id)
    return render_template('customer_details_for_staff.html',
                           customer=customer,
                           orders=orders,
                           payments=payments)
