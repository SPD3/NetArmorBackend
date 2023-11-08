from src.database import Database
from tests.constants import CSRF_NAME, CSRF_DATE_ADDED, MINNIE_SCAN_ID, MINNIE_EMAIL, MINNIE_URL, MINNIE_DEEP, MINNIE_DATE
from src.vulnerability_functions import add_vulnerability, add_sqli_vulnerability, check_vulnerability, check_sqli_vulnerability, check_found_sqli, add_found_sqli, add_found_vulnerability, check_found_vulnerability
from tests.test_main import generic_add_test, generic_duplicate_test
from src.scan_functions import add_mickey_scan, add_scan
from tests.helpers import add_mickey, add_websites, add_vulnerabilities
from src.website_functions import add_mickey_website

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