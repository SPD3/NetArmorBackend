from sqlalchemy.exc import IntegrityError
import pytest
from src.database import Database
from tests.constants import XSS_NAME, XSS_DATE_ADDED, MINNIE_EMAIL, MINNIE_URL, SQLI_NAME, MICKEY_EMAIL, MICKEY_URL, SQLI_DATE, SQLI_DESCRIPTION, XSS_DESCRIPTION, MICKEY_SCAN_SCORE, MINNIE_SCAN_SCORE, SQLI_SUCCESS, XSS_SUCCESS
from src.vulnerability_functions import add_vulnerability, check_vulnerability, add_tested_vulnerability, check_tested_vulnerability
from tests.test_main import generic_add_test, generic_duplicate_test
from tests.helpers.vulnerability_helpers import add_mock_tested_vulnerability
from datetime import timedelta
from psycopg2.errors import UniqueViolation


def test_add_vulnerability_table():
    db_session = Database().get_session()    
    generic_add_test(lambda: check_vulnerability(db_session,SQLI_NAME, SQLI_DATE),
                     lambda: add_vulnerability(db_session, SQLI_NAME, SQLI_DATE), 
                     lambda: check_vulnerability(db_session, XSS_NAME, XSS_DATE_ADDED),
                     lambda: add_vulnerability(db_session, XSS_NAME, XSS_DATE_ADDED))
    db_session.rollback()

def test_duplicate_vulnerability_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                           lambda: add_vulnerability(db_session, SQLI_NAME, SQLI_DATE),
                           lambda: add_vulnerability(db_session, SQLI_NAME, SQLI_DATE-timedelta(days=1)))
    db_session.rollback()
    
def test_add_tested_vulnerability():
    db_session = Database().get_session()
    
    scan_id = add_mock_tested_vulnerability(db_session, SQLI_NAME, MICKEY_SCAN_SCORE, SQLI_SUCCESS, SQLI_DESCRIPTION, MICKEY_EMAIL, MICKEY_URL)
    assert check_tested_vulnerability(db_session, scan_id, SQLI_NAME, MICKEY_SCAN_SCORE, SQLI_SUCCESS, SQLI_DESCRIPTION)
    scan_id = add_mock_tested_vulnerability(db_session, XSS_NAME, MINNIE_SCAN_SCORE, XSS_SUCCESS, XSS_DESCRIPTION, MINNIE_EMAIL, MINNIE_URL)
    assert check_tested_vulnerability(db_session, scan_id, XSS_NAME, MINNIE_SCAN_SCORE, XSS_SUCCESS, XSS_DESCRIPTION)

    db_session.rollback()

def test_duplicate_tested_vulnerability():
    db_session = Database().get_session()

    scan_id = add_mock_tested_vulnerability(db_session, SQLI_NAME, MICKEY_SCAN_SCORE, SQLI_SUCCESS, SQLI_DESCRIPTION)
    with pytest.raises(IntegrityError) as e:
        add_tested_vulnerability(db_session, scan_id, SQLI_NAME, MICKEY_SCAN_SCORE-20, not SQLI_SUCCESS, SQLI_DESCRIPTION+"a")
        db_session.commit()
    assert isinstance(e.value.orig, UniqueViolation)
    
    db_session.rollback()