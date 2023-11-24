from src.database import Database
from tests.constants import DAISY_EMAIL, MINNIE_EMAIL, DONALD_EMAIL, MICKEY_EMAIL, MICKEY_PAYLOAD, MICKEY_SENT_TIME, MINNIE_PAYLOAD, MINNIE_SENT_TIME, MICKEY_STATUS, MINNIE_STATUS
from tests.test_main import generic_add_test, generic_duplicate_test
from tests.helpers.message_helpers import add_mock_message
from src.message_functions import check_message, add_message
from datetime import timedelta

def test_add_message():
    db_session = Database().get_session()
    generic_add_test(lambda: check_message(db_session, MICKEY_EMAIL, DONALD_EMAIL, MICKEY_PAYLOAD, MICKEY_STATUS, MICKEY_SENT_TIME), 
                     lambda: add_mock_message(db_session, MICKEY_EMAIL, DONALD_EMAIL, MICKEY_PAYLOAD, MICKEY_STATUS, MICKEY_SENT_TIME), 
                     lambda: check_message(db_session, MINNIE_EMAIL, DAISY_EMAIL, MINNIE_PAYLOAD, MINNIE_STATUS, MINNIE_SENT_TIME),
                     lambda: add_mock_message(db_session, MINNIE_EMAIL, DAISY_EMAIL, MINNIE_PAYLOAD, MINNIE_STATUS, MINNIE_SENT_TIME))
    db_session.rollback()

def test_duplicate_message():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                           lambda: add_mock_message(db_session, MICKEY_EMAIL, DONALD_EMAIL, MICKEY_PAYLOAD, MICKEY_STATUS, MICKEY_SENT_TIME),
                           lambda: add_message(db_session, MICKEY_EMAIL, DONALD_EMAIL, MICKEY_PAYLOAD+"a", not MICKEY_STATUS, MICKEY_SENT_TIME-timedelta(hours=1)))
    db_session.rollback()