from src.database import Database
from tests.constants import CSRF_NAME, CSRF_DATE_ADDED, MINNIE_SCAN_ID, MINNIE_EMAIL, MINNIE_URL, SQLI_NAME, MICKEY_SCAN_ID, MICKEY_EMAIL, MICKEY_URL, SQLI_DATE, SQLI_DESCRIPTION, CSRF_DESCRIPTION, MICKEY_SCAN_SCORE, MINNIE_SCAN_SCORE, SQLI_SUCCESS, CSRF_SUCCESS
from src.vulnerability_functions import add_vulnerability, check_vulnerability, add_tested_vulnerability, check_tested_vulnerability
from tests.test_main import generic_add_test, generic_duplicate_test
from tests.helpers.vulnerability_helpers import add_mock_tested_vulnerability
from datetime import timedelta


def test_add_vulnerability_table():
    db_session = Database().get_session()    
    generic_add_test(lambda: check_vulnerability(db_session,SQLI_NAME, SQLI_DATE),
                     lambda: add_vulnerability(db_session, SQLI_NAME, SQLI_DATE), 
                     lambda: check_vulnerability(db_session, CSRF_NAME, CSRF_DATE_ADDED),
                     lambda: add_vulnerability(db_session, CSRF_NAME, CSRF_DATE_ADDED))
    db_session.rollback()

def test_duplicate_vulnerability_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                           lambda: add_vulnerability(db_session, SQLI_NAME, SQLI_DATE),
                           lambda: add_vulnerability(db_session, SQLI_NAME, SQLI_DATE-timedelta(days=1)))
    db_session.rollback()
    
def test_add_tested_vulnerability():
    db_session = Database().get_session()
    generic_add_test(lambda: check_tested_vulnerability(db_session, MICKEY_SCAN_ID, SQLI_NAME, MICKEY_SCAN_SCORE, SQLI_SUCCESS, SQLI_DESCRIPTION),
                     lambda: add_mock_tested_vulnerability(db_session, MICKEY_SCAN_ID, SQLI_NAME, MICKEY_SCAN_SCORE, SQLI_SUCCESS, SQLI_DESCRIPTION, MICKEY_EMAIL, MICKEY_URL), 
                     lambda: check_tested_vulnerability(db_session, MINNIE_SCAN_ID, CSRF_NAME, MINNIE_SCAN_SCORE, CSRF_SUCCESS, CSRF_DESCRIPTION),
                     lambda: add_mock_tested_vulnerability(db_session, MINNIE_SCAN_ID, CSRF_NAME, MINNIE_SCAN_SCORE, CSRF_SUCCESS, CSRF_DESCRIPTION, MINNIE_EMAIL, MINNIE_URL))
    db_session.rollback()

def test_duplicate_tested_vulnerability():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                           lambda: add_mock_tested_vulnerability(db_session, MICKEY_SCAN_ID, SQLI_NAME, MICKEY_SCAN_SCORE, SQLI_SUCCESS, SQLI_DESCRIPTION), 
                           lambda: add_tested_vulnerability(db_session, MICKEY_SCAN_ID, SQLI_NAME, MICKEY_SCAN_SCORE-20, not SQLI_SUCCESS, SQLI_DESCRIPTION+"a"))
    db_session.rollback()