from fhv.dao.user_dao import UserDAO
from fhv.models import Person


def test_get_person_by_username(init_database):
    dao = UserDAO()
    person = dao.get_person_by_username("pcustomer4")
    assert person is not None
    assert person.username == "pcustomer4"


def test_get_person_by_username_not_found(init_database):
    dao = UserDAO()
    person = dao.get_person_by_username("none_existent")
    assert person is None


def test_check_password(init_database):
    dao = UserDAO()
    person = Person(firstname='Bob', lastname='James',
                    username='pcustomer4', password='pcustomer123')
    assert dao.check_password(person, "pcustomer123") is True


def test_check_password_invalid(init_database):
    dao = UserDAO()
    person = Person(firstname='Bob', lastname='James',
                    username='pcustomer4', password='pcustomer123')
    assert dao.check_password(person, "incorrect") is False
