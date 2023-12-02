from src.database import Database
from tests.constants import MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_URL, MINNIE_WEBSITE_NAME, MINNIE_IMAGE, MICKEY_EMAIL, MICKEY_URL, MICKEY_WEBSITE_NAME, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE, MINNIE_IMAGE, MICKEY_COOKIE, MINNIE_COOKIE
from src.website_functions import add_website, add_website_owner, check_website, check_website_owner, check_cookie_exists_for_email, add_cookie
from tests.test_main import generic_add_test, generic_duplicate_test
from tests.helpers.website_helpers import add_mock_website, add_mock_website_owner_cookie
from src.main import check_website_owner_credentials, create_website_owner, website_owner_exists, delete_website_owner

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
                           lambda: add_website_owner(db_session, MICKEY_EMAIL, MINNIE_PASSWORD, MICKEY_FIRST_NAME+"a", MICKEY_LAST_NAME+"a", MICKEY_IMAGE+"a"))
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
                           lambda: add_website(db_session, MICKEY_URL, MICKEY_EMAIL+"a", MICKEY_WEBSITE_NAME+"a"))
    db_session.rollback()

def test_add_cookie():
    db_session = Database().get_session()
    generic_add_test(lambda: check_cookie_exists_for_email(db_session, MICKEY_COOKIE, MICKEY_EMAIL),
                     lambda: add_mock_website_owner_cookie(db_session, MICKEY_COOKIE, MICKEY_EMAIL), 
                     lambda: check_cookie_exists_for_email(db_session, MINNIE_COOKIE, MINNIE_EMAIL),
                     lambda: add_mock_website_owner_cookie(db_session, MINNIE_COOKIE, MINNIE_EMAIL))
    db_session.rollback()

def test_duplicate_cookie():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                           lambda: add_mock_website_owner_cookie(db_session, MICKEY_COOKIE, MICKEY_EMAIL), 
                           lambda: add_cookie(db_session, MICKEY_COOKIE, True, MICKEY_EMAIL))
    db_session.rollback()
    
def test_create_website_owner():
    db_session = Database().get_session()
    generic_add_test(lambda: check_website_owner(db_session, MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE), 
                    lambda: create_website_owner(MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE), 
                    lambda: check_website_owner(db_session, MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE),
                    lambda: create_website_owner(MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE))
    delete_website_owner(MICKEY_EMAIL)
    delete_website_owner(MINNIE_EMAIL)
    db_session.rollback()
    
def test_website_owner_exists():
    generic_add_test(lambda: website_owner_exists(MICKEY_EMAIL),
                    lambda: create_website_owner(MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE), 
                    lambda: website_owner_exists(MINNIE_EMAIL),
                    lambda: create_website_owner(MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE))
    delete_website_owner(MICKEY_EMAIL)
    delete_website_owner(MINNIE_EMAIL)
    
def test_check_website_owner_credentials():
    create_website_owner(MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE)
    assert (check_website_owner_credentials(MICKEY_EMAIL, MICKEY_PASSWORD) == True 
            and check_website_owner_credentials(MICKEY_EMAIL, MINNIE_PASSWORD) == False)
    delete_website_owner(MICKEY_EMAIL)
    
def test_delete_website_owner():
    create_website_owner(MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE)
    assert (website_owner_exists(MICKEY_EMAIL) == True)
    assert (delete_website_owner(MICKEY_EMAIL) == True)
    assert (website_owner_exists(MICKEY_EMAIL) == False)
    delete_website_owner(MICKEY_EMAIL)

    