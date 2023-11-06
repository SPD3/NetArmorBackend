from tests.test_main import *

def test_add_scan():
    db_session = Database().get_session()
    add_websites(db_session)
    generic_add_test(lambda: check_mickey_scan(db_session), 
                     lambda: add_mickey_scan(db_session), 
                     lambda: check_scan(db_session, MINNIE_SCAN_ID, MINNIE_EMAIL, MINNIE_URL, MINNIE_DEEP, MINNIE_DATE),
                     lambda: add_scan(db_session, MINNIE_SCAN_ID, MINNIE_EMAIL, MINNIE_URL, MINNIE_DEEP, MINNIE_DATE))
    db_session.rollback()

def test_duplicate_scan():
    db_session = Database().get_session()
    add_mickey(db_session)
    add_mickey_website(db_session)
    generic_duplicate_test(db_session, lambda: add_mickey_scan(db_session))
    db_session.rollback()