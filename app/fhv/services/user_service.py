from flask import session
from fhv.dao.user_dao import UserDAO


class LoginService:
    def __init__(self, person_dao: UserDAO):
        self.person_dao = person_dao

    def login(self, username: str, password: str):
        person = self.person_dao.get_person_by_username(username)

        if person and person.check_password(password):
            session['user_id'] = person.id
            session['user_username'] = person.username
            session['user_type'] = person.type
            if person.type == 'staff':
                session['department'] = person.department
            elif person.type == 'customer':
                session['balance'] = person.balance
                session['address'] = person.address
            elif person.type == 'corporate_customer':
                session['balance'] = person.balance
                session['address'] = person.address
                session['credit_limit'] = person.credit_limit
            if person.address == 'Riccarton Chch' or person.address == 'Addington Chch':
                session['deliverable'] = True
            else:
                session['deliverable'] = False
            return {"success": True, "message": "Login successful", "user": person.username, "type": person.type}
        else:
            return {"success": False, "message": "Invalid username or password"}
