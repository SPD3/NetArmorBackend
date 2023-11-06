from tests.test_main import *


def test_add_vulnerability_table():
    db_session = Database().get_session()    
    generic_add_test(lambda: check_sqli_vulnerability(db_session), 
                     lambda: add_sqli_vulnerability(db_session), 
                     lambda: check_vulnerability(db_session, CSRF_NAME, CSRF_DATE_ADDED),
                     lambda: add_vulnerability(db_session, CSRF_NAME, CSRF_DATE_ADDED))
    db_session.rollback()

def test_duplicate_vulnerability_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, lambda: add_sqli_vulnerability(db_session))
    db_session.rollback()
    
def test_add_found_vulnerability():
    db_session = Database().get_session()
    add_websites(db_session)
    add_vulnerabilities(db_session)
    add_mickey_scan(db_session)
    add_scan(db_session, MINNIE_SCAN_ID, MINNIE_EMAIL, MINNIE_URL, MINNIE_DEEP, MINNIE_DATE)
    generic_add_test(lambda: check_found_sqli(db_session), 
                     lambda: add_found_sqli(db_session), 
                     lambda: check_found_vulnerability(db_session, MINNIE_SCAN_ID, CSRF_NAME),
                     lambda: add_found_vulnerability(db_session, MINNIE_SCAN_ID, CSRF_NAME))
    db_session.rollback()

def test_duplicate_found_vulnerability():
    db_session = Database().get_session()
    add_mickey(db_session)
    add_mickey_website(db_session)
    add_mickey_scan(db_session)
    add_sqli_vulnerability(db_session)
    generic_duplicate_test(db_session, lambda: add_found_sqli(db_session))
    db_session.rollback()