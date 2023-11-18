import pytest
from src.database import Database
from tests.constants import DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME, DAISY_RATING, DAISY_IMAGE, MINNIE_EMAIL, CSRF_NAME, DONALD_EMAIL, MICKEY_EMAIL, SQLI_NAME
from tests.test_main import generic_add_test, generic_duplicate_test
from src.expert_functions import check_cybersecurity_expert, add_cybersecurity_expert, check_cybersecurity_expert_rating, add_cybersecurity_expert_rating, check_specialty, add_specialty
from tests.helpers.helper import add_cybersecurity_experts, add_website_owners, add_vulnerabilities
from tests.helpers.website_helpers import add_mickey
from tests.helpers.vulnerability_helpers import add_sqli_vulnerability
from tests.helpers.expert_helpers import add_donald, check_donald, add_donald_rating, check_donald_rating, add_donald_specialty, check_donald_specialty

def test_add_cybersecurity_expert_table():
    db_session = Database().get_session()
    generic_add_test(lambda: check_donald(db_session), 
                     lambda: add_donald(db_session), 
                     lambda: check_cybersecurity_expert(db_session, DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME, DAISY_IMAGE),
                     lambda: add_cybersecurity_expert(db_session, DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME, DAISY_IMAGE))
    db_session.rollback()

def test_duplicate_cybersecurity_expert_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                lambda: add_donald(db_session),
                lambda: add_cybersecurity_expert(db_session, DONALD_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME, DAISY_IMAGE))
    db_session.rollback()
    
def test_add_expert_rating():
    db_session = Database().get_session()
    add_website_owners(db_session)  
    add_cybersecurity_experts(db_session)
    generic_add_test(lambda: check_donald_rating(db_session), 
                     lambda: add_donald_rating(db_session), 
                     lambda: check_cybersecurity_expert_rating(db_session, MINNIE_EMAIL, DAISY_EMAIL, DAISY_RATING),
                     lambda: add_cybersecurity_expert_rating(db_session, MINNIE_EMAIL, DAISY_EMAIL, DAISY_RATING))
    db_session.rollback()

def test_duplicate_expert_rating():
    db_session = Database().get_session()
    add_mickey(db_session)
    add_donald(db_session)
    generic_duplicate_test(db_session, 
                           lambda: add_donald_rating(db_session),
                           lambda: add_cybersecurity_expert_rating(db_session, MICKEY_EMAIL, DONALD_EMAIL, DAISY_RATING))
    db_session.rollback()
    
# @pytest.fixture()
# def micky_website():
#     # create micky Website
#     yield
#     # delete micky Website

# @pytest.fixture()
# def micky_expert(micky_website):
#     print("1")
#     # create micky expert entry
#     yield add_donald_specialty
#     # delete micky expert entry
#     print("2")
    
# def test_add_specialty_table(micky_expert):
def test_add_specialty_table():
    db_session = Database().get_session()
    add_vulnerabilities(db_session)
    add_cybersecurity_experts(db_session)   
    generic_add_test(lambda: check_donald_specialty(db_session), 
                     lambda: add_donald_specialty(db_session), 
                     lambda: check_specialty(db_session, DAISY_EMAIL, CSRF_NAME),
                     lambda: add_specialty(db_session, DAISY_EMAIL, CSRF_NAME))
    db_session.rollback()

def test_duplicate_specialty_table():
    db_session = Database().get_session()
    add_donald(db_session)
    add_sqli_vulnerability(db_session)
    generic_duplicate_test(db_session, 
                lambda: add_donald_specialty(db_session),
                lambda: add_specialty(db_session, DONALD_EMAIL, SQLI_NAME))
    db_session.rollback()