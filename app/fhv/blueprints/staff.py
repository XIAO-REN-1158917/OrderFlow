from flask import Blueprint, redirect
from flask import render_template
from flask import request
from fhv.services.user_service import LoginService
from fhv.dao.user_dao import UserDAO

bp = Blueprint('staff', __name__, url_prefix='/staff')


@bp.route('/index')
def index():
    return render_template('staffIndex.html')
