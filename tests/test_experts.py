import pytest
from src.database import Database
from tests.constants import DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME, DAISY_RATING, DAISY_IMAGE, MINNIE_EMAIL, XSS_NAME, DONALD_EMAIL, MICKEY_EMAIL, SQLI_NAME, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE, DONALD_RATING, TEST_IMAGE
from tests.test_main import generic_add_test, generic_duplicate_test
from src.expert_functions import check_cybersecurity_expert, add_cybersecurity_expert, check_cybersecurity_expert_rating, add_cybersecurity_expert_rating, check_specialty, add_specialty
from tests.helpers.expert_helpers import add_mock_expert_rating, add_mock_specialty
from src.expert_endpoints import check_expert_info, expert_exists, create_expert_account, delete_expert, add_expert_info
from src.populate_tables import populate_vulnerabilities
from datetime import date
from src import models


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
                lambda: add_cybersecurity_expert(db_session, DONALD_EMAIL, DONALD_PASSWORD+"a", DONALD_FIRST_NAME+"a", DONALD_LAST_NAME+"a", DONALD_IMAGE+"a"))
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
                           lambda: add_cybersecurity_expert_rating(db_session, MICKEY_EMAIL, DONALD_EMAIL, DONALD_RATING-1))
    db_session.rollback()
    
def test_add_specialty_table():
    db_session = Database().get_session()
    generic_add_test(lambda: check_specialty(db_session, DONALD_EMAIL, SQLI_NAME), 
                     lambda: add_mock_specialty(db_session, DONALD_EMAIL, SQLI_NAME), 
                     lambda: check_specialty(db_session, DAISY_EMAIL, XSS_NAME),
                     lambda: add_mock_specialty(db_session, DAISY_EMAIL, XSS_NAME))
    db_session.rollback()

def test_duplicate_specialty_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                lambda: add_mock_specialty(db_session, DONALD_EMAIL, SQLI_NAME),
                lambda: add_specialty(db_session, DONALD_EMAIL, SQLI_NAME))
    db_session.rollback()
    
def test_create_expert_account():
    db_session = Database().get_session()
    generic_add_test(lambda: check_cybersecurity_expert(db_session, DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, TEST_IMAGE), 
                    lambda: create_expert_account(DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME), 
                    lambda: check_cybersecurity_expert(db_session, DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME, TEST_IMAGE),
                    lambda: create_expert_account(DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME))
    db_session.rollback()
    
def test_expert_exists():
    generic_add_test(lambda: expert_exists(DONALD_EMAIL),
                    lambda: create_expert_account(DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME), 
                    lambda: expert_exists(DAISY_EMAIL),
                    lambda: create_expert_account(DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME))
    
def test_check_expert_info():
    create_expert_account(DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME)
    assert (check_expert_info(DONALD_EMAIL, DONALD_PASSWORD) == True 
            and check_expert_info(DONALD_EMAIL, DAISY_PASSWORD) == False)
    
def test_delete_expert():
    create_expert_account(DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME)
    assert (expert_exists(DONALD_EMAIL) == True)
    assert (delete_expert(DONALD_EMAIL) == True)
    assert (expert_exists(DONALD_EMAIL) == False)

def test_add_expert_info():
    populate_vulnerabilities()
    create_expert_account(DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME)
    add_expert_info(DONALD_EMAIL, DONALD_IMAGE, True, True, False, False)
    db = Database().get_session()
    query = db.query(models.Specialty).filter(models.Specialty.expert == DONALD_EMAIL).all()
    assert (len(query) == 2)
    vulnerability_set = set()
    for vulnerability in query:
        assert (vulnerability.expert == DONALD_EMAIL)
        vulnerability_set.add(vulnerability.vulnerability)
    assert ("SQL Injection" in vulnerability_set and "Cross-Site Scripting" in vulnerability_set)
