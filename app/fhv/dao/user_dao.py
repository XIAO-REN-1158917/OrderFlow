from fhv.models import Person, Customer, CorporateCustomer
from fhv.exts import db


class UserDAO:
    def get_person_by_username(self, username: str):
        return Person.query.filter_by(username=username).first()
