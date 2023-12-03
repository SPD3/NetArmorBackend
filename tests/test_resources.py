from src.database import Database
from tests.constants import XSS_LINK, XSS_TITLE, XSS_NAME, MINNIE_EMAIL, XSS_RATING, SQLI_LINK, MICKEY_EMAIL, SQLI_NAME, SQLI_TITLE, SQLI_RATING
from tests.test_main import generic_add_test, generic_duplicate_test
from src.resource_functions import check_resource, add_resource, check_resource_rating, add_resource_rating
from tests.helpers.resource_helpers import add_mock_resource, add_mock_resource_rating


def test_add_resource_table():
    db_session = Database().get_session()
    generic_add_test(lambda: check_resource(db_session, SQLI_LINK, SQLI_TITLE, SQLI_NAME), 
                     lambda: add_mock_resource(db_session, SQLI_LINK, SQLI_TITLE, SQLI_NAME), 
                     lambda: check_resource(db_session, XSS_LINK, XSS_TITLE, XSS_NAME),
                     lambda: add_mock_resource(db_session, XSS_LINK, XSS_TITLE, XSS_NAME))
    db_session.rollback()

def test_duplicate_resource_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                           lambda: add_mock_resource(db_session, SQLI_LINK, SQLI_TITLE, SQLI_NAME),
                           lambda: add_resource(db_session, SQLI_LINK, SQLI_TITLE+"a", SQLI_NAME+"a"))
    db_session.rollback()

def test_add_resource_rating():
    db_session = Database().get_session()
    generic_add_test(lambda: check_resource_rating(db_session, MICKEY_EMAIL, SQLI_LINK, SQLI_RATING), 
                     lambda: add_mock_resource_rating(db_session, MICKEY_EMAIL, SQLI_LINK, SQLI_RATING, SQLI_NAME), 
                     lambda: check_resource_rating(db_session, MINNIE_EMAIL, XSS_LINK, XSS_RATING),
                     lambda: add_mock_resource_rating(db_session, MINNIE_EMAIL, XSS_LINK, XSS_RATING, XSS_NAME))
    db_session.rollback()

def test_duplicate_resource_rating():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                           lambda: add_mock_resource_rating(db_session, MICKEY_EMAIL, SQLI_LINK, SQLI_RATING, SQLI_NAME),
                           lambda: add_resource_rating(db_session, MICKEY_EMAIL, SQLI_LINK, SQLI_RATING-1))
    db_session.rollback()