from src.database import Database
from tests.constants import MINNIE_EMAIL, MINNIE_URL,  MINNIE_SCAN_ID, MINNIE_DEEP, MINNIE_DATE, MICKEY_SCAN_ID 
from src.scan_functions import add_scan,  check_scan
from tests.test_main import generic_add_test, generic_duplicate_test
from tests.helpers.helper import add_websites
from tests.helpers.scan_helpers import add_mickey_scan, check_mickey_scan
from tests.helpers.website_helpers import add_mickey_website, add_mickey

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
    generic_duplicate_test(db_session, 
                           lambda: add_mickey_scan(db_session),
                           lambda: add_scan(db_session, MICKEY_SCAN_ID, MINNIE_EMAIL, MINNIE_URL, MINNIE_DEEP, MINNIE_DATE))
    db_session.rollback()