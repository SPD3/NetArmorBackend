from tests.test_main import *
  

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