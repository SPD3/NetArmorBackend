from src.database import Database
from tests.constants import MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_URL, MINNIE_WEBSITE_NAME
from src.website_functions import add_mickey_website, add_website, add_website_owner, add_mickey, check_mickey_website, check_website, check_website_owner, check_mickey
from tests.test_main import generic_add_test, generic_duplicate_test
from tests.helpers import add_website_owners, add_mickey

def test_add_website_owner_table():
    db_session = Database().get_session()
    generic_add_test(lambda: check_mickey(db_session), 
                     lambda: add_mickey(db_session), 
                     lambda: check_website_owner(db_session, MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME),
                     lambda: add_website_owner(db_session, MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME))
    db_session.rollback()

def test_duplicate_websiste_owner_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, lambda: add_mickey(db_session))
    db_session.rollback()
    
def test_add_website_table():
    db_session = Database().get_session()
    add_website_owners(db_session)
    generic_add_test(lambda: check_mickey_website(db_session), 
                     lambda: add_mickey_website(db_session), 
                     lambda: check_website(db_session, MINNIE_URL, MINNIE_EMAIL, MINNIE_WEBSITE_NAME),
                     lambda: add_website(db_session, MINNIE_URL, MINNIE_EMAIL, MINNIE_WEBSITE_NAME))
    db_session.rollback()

def test_duplicate_website_table():
    db_session = Database().get_session()
    add_mickey(db_session)
    generic_duplicate_test(db_session, lambda: add_mickey_website(db_session))
    db_session.rollback()