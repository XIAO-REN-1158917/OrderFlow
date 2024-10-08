from flask import Blueprint, redirect, url_for
from flask import render_template
from flask import request
from fhv.services.user_service import LoginService
from fhv.dao.user_dao import UserDAO

bp = Blueprint('user', __name__, url_prefix='/')


@bp.route('/')
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        person_dao = UserDAO()
        login_service = LoginService(person_dao)

        result = login_service.login(username, password)

        if result['success']:
            if result['type'] == 'staff':
                return redirect(url_for('staff.index'))
            elif result['type'] == 'customer' or result['type'] == 'corporate_customer':
                return redirect(url_for('customer.index'))
            else:
                return redirect(url_for('login'))
        else:
            return render_template('login.html', error=result['message'])

    else:
        return render_template('login.html')
