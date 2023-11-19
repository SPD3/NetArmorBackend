from src.database import Database
from tests.constants import MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_URL, MINNIE_WEBSITE_NAME, MINNIE_IMAGE, MICKEY_EMAIL, MICKEY_URL, MICKEY_WEBSITE_NAME, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE, MINNIE_IMAGE
from src.website_functions import add_website, add_website_owner, check_website, check_website_owner
from tests.test_main import generic_add_test, generic_duplicate_test
from tests.helpers.website_helpers import add_mock_website

def test_add_website_owner_table():
    db_session = Database().get_session()
    generic_add_test(lambda: check_website_owner(db_session, MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE), 
                     lambda: add_website_owner(db_session, MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE), 
                     lambda: check_website_owner(db_session, MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE),
                     lambda: add_website_owner(db_session, MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE))
    db_session.rollback()

def test_duplicate_websiste_owner_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                           lambda: add_website_owner(db_session, MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE), 
                           lambda: add_website_owner(db_session, MICKEY_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE))
    db_session.rollback()
    
def test_add_website_table():
    db_session = Database().get_session()
    generic_add_test(lambda: check_website(db_session, MICKEY_URL, MICKEY_EMAIL, MICKEY_WEBSITE_NAME),
                     lambda: add_mock_website(db_session, MICKEY_URL, MICKEY_EMAIL, MICKEY_WEBSITE_NAME), 
                     lambda: check_website(db_session, MINNIE_URL, MINNIE_EMAIL, MINNIE_WEBSITE_NAME),
                     lambda: add_mock_website(db_session, MINNIE_URL, MINNIE_EMAIL, MINNIE_WEBSITE_NAME))
    db_session.rollback()

def test_duplicate_website_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                           lambda: add_mock_website(db_session, MICKEY_URL, MICKEY_EMAIL, MICKEY_WEBSITE_NAME), 
                           lambda: add_website(db_session, MICKEY_URL, MINNIE_EMAIL, MINNIE_WEBSITE_NAME))
    db_session.rollback()