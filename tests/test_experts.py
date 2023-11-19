import pytest
from src.database import Database
from tests.constants import DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME, DAISY_RATING, DAISY_IMAGE, MINNIE_EMAIL, CSRF_NAME, DONALD_EMAIL, MICKEY_EMAIL, SQLI_NAME, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE, DONALD_RATING
from tests.test_main import generic_add_test, generic_duplicate_test
from src.expert_functions import check_cybersecurity_expert, add_cybersecurity_expert, check_cybersecurity_expert_rating, add_cybersecurity_expert_rating, check_specialty, add_specialty
from tests.helpers.expert_helpers import add_mock_expert_rating, add_mock_specialty

def test_add_cybersecurity_expert_table():
    db_session = Database().get_session()
    generic_add_test(lambda: check_cybersecurity_expert(db_session, DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE), 
                     lambda: add_cybersecurity_expert(db_session, DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE), 
                     lambda: check_cybersecurity_expert(db_session, DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME, DAISY_IMAGE),
                     lambda: add_cybersecurity_expert(db_session, DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME, DAISY_IMAGE))
    db_session.rollback()

def test_duplicate_cybersecurity_expert_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                lambda: add_cybersecurity_expert(db_session, DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE),
                lambda: add_cybersecurity_expert(db_session, DONALD_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME, DAISY_IMAGE))
    db_session.rollback()
    
def test_add_expert_rating():
    db_session = Database().get_session()
    generic_add_test(lambda: check_cybersecurity_expert_rating(db_session, MICKEY_EMAIL, DONALD_EMAIL, DONALD_RATING), 
                     lambda: add_mock_expert_rating(db_session, MICKEY_EMAIL, DONALD_EMAIL, DONALD_RATING), 
                     lambda: check_cybersecurity_expert_rating(db_session, MINNIE_EMAIL, DAISY_EMAIL, DAISY_RATING),
                     lambda: add_mock_expert_rating(db_session, MINNIE_EMAIL, DAISY_EMAIL, DAISY_RATING))
    db_session.rollback()

def test_duplicate_expert_rating():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                           lambda: add_mock_expert_rating(db_session, MICKEY_EMAIL, DONALD_EMAIL, DONALD_RATING),
                           lambda: add_cybersecurity_expert_rating(db_session, MICKEY_EMAIL, DONALD_EMAIL, DAISY_RATING))
    db_session.rollback()
    
def test_add_specialty_table():
    db_session = Database().get_session()
    generic_add_test(lambda: check_specialty(db_session, DONALD_EMAIL, SQLI_NAME), 
                     lambda: add_mock_specialty(db_session, DONALD_EMAIL, SQLI_NAME), 
                     lambda: check_specialty(db_session, DAISY_EMAIL, CSRF_NAME),
                     lambda: add_mock_specialty(db_session, DAISY_EMAIL, CSRF_NAME))
    db_session.rollback()

def test_duplicate_specialty_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                lambda: add_mock_specialty(db_session, DONALD_EMAIL, SQLI_NAME),
                lambda: add_specialty(db_session, DONALD_EMAIL, SQLI_NAME))
    db_session.rollback()