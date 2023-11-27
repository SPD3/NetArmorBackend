from src.database import Database
from tests.constants import MINNIE_EMAIL, MINNIE_URL, MINNIE_SCAN_ID, MINNIE_DEEP, MINNIE_SCAN_DATE, MICKEY_SCAN_ID, MICKEY_EMAIL, MICKEY_URL, MICKEY_DEEP, MICKEY_SCAN_DATE, MICKEY_SCAN_SCORE, MINNIE_SCAN_SCORE
from src.scan_functions import add_scan,  check_scan
from tests.test_main import generic_add_test, generic_duplicate_test
from tests.helpers.scan_helpers import add_mock_scan
from datetime import timedelta

def test_add_scan():
    db_session = Database().get_session()
    generic_add_test(lambda: check_scan(db_session, MICKEY_SCAN_ID, MICKEY_EMAIL, MICKEY_URL, MICKEY_DEEP, MICKEY_SCAN_DATE), 
                     lambda: add_mock_scan(db_session, MICKEY_SCAN_ID, MICKEY_EMAIL, MICKEY_URL, MICKEY_DEEP, MICKEY_SCAN_DATE), 
                     lambda: check_scan(db_session, MINNIE_SCAN_ID, MINNIE_EMAIL, MINNIE_URL, MINNIE_DEEP, MINNIE_SCAN_DATE),
                     lambda: add_mock_scan(db_session, MINNIE_SCAN_ID, MINNIE_EMAIL, MINNIE_URL,  MINNIE_DEEP, MINNIE_SCAN_DATE))
    db_session.rollback()

def test_duplicate_scan():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                           lambda: add_mock_scan(db_session, MICKEY_SCAN_ID, MICKEY_EMAIL, MICKEY_URL, MICKEY_DEEP, MICKEY_SCAN_DATE),
                           lambda: add_scan(db_session, MICKEY_SCAN_ID, MICKEY_EMAIL+"a", MICKEY_URL+"a", not MICKEY_DEEP, MICKEY_SCAN_DATE-timedelta(days=1)))
    db_session.rollback()