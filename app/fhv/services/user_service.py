from flask import session
from fhv.dao.user_dao import UserDAO


class LoginService:
    def __init__(self, person_dao: UserDAO):
        self.person_dao = person_dao

    def login(self, username: str, password: str):
        person = self.person_dao.get_person_by_username(username)

        if person and person.check_password(password):
            session['user_id'] = person.id
            session['user_type'] = person.type
            return {"success": True, "message": "Login successful", "user": person.username, "type": person.type}
        else:
            return {"success": False, "message": "Invalid username or password"}
