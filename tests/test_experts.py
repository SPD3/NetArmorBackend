import pytest
from src.database import Database
from tests.constants import DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME, DAISY_RATING, DAISY_IMAGE, MINNIE_EMAIL, XSS_NAME, DONALD_EMAIL, MICKEY_EMAIL, SQLI_NAME, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE, DONALD_RATING, TEST_IMAGE, PENTEST_IMAGE, CLOUD_IMAGE, MICKEY_IMAGE, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE, MICKEY_MESSAGE, MINNIE_MESSAGE, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE, XSS_DATE_ADDED, SQLI_DATE_ADDED
from tests.test_main import generic_add_test, generic_duplicate_test
from src.expert_functions import check_cybersecurity_expert, add_cybersecurity_expert, check_cybersecurity_expert_rating, add_cybersecurity_expert_rating, check_specialty, add_specialty, delete_specialty
from tests.helpers.expert_helpers import add_mock_expert_rating, add_mock_specialty
from src.expert_endpoints import check_expert_info, expert_exists, create_expert_account, delete_expert, add_expert_info, get_expert_info, remove_client, update_expert_info
from src.populate_tables import populate_vulnerabilities, SQL_INJECTION_NAME, NMAP_NAME, JWT_COOKIE_HIJACKING_NAME
from src.certificate_endpoints import add_cert
from src import models
from src.website_owner_endpoints import create_expert_request
from src.main import create_website_owner
from src import crud
from src.vulnerability_functions import add_vulnerability



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

def test_get_expert_info():
    populate_vulnerabilities()
    create_expert_account(DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME)
    add_expert_info(DONALD_EMAIL, DONALD_IMAGE, True, True, False, False)
    add_cert(PENTEST_IMAGE, DONALD_EMAIL)
    add_cert(CLOUD_IMAGE, DONALD_EMAIL)
    create_website_owner(MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE)
    create_website_owner(MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE)
    create_expert_request(MICKEY_EMAIL, DONALD_EMAIL, MICKEY_MESSAGE)
    create_expert_request(MINNIE_EMAIL, DONALD_EMAIL, MINNIE_MESSAGE)
    result = get_expert_info(DONALD_EMAIL)
    assert(result["email"] == DONALD_EMAIL and result["password"] == DONALD_PASSWORD 
           and result["first_name"] == DONALD_FIRST_NAME and result["last_name"] == DONALD_LAST_NAME
           and result["image"] == DONALD_IMAGE and result["certifications"] == [PENTEST_IMAGE, CLOUD_IMAGE]
           and result["specialties"] == ["SQL Injection", "Cross-Site Scripting"]
           and result["clients"] == [MICKEY_EMAIL, MINNIE_EMAIL])

def test_remove_client():
    create_expert_account(DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME)
    create_website_owner(MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE)
    create_website_owner(MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE)
    create_expert_request(MICKEY_EMAIL, DONALD_EMAIL, MICKEY_MESSAGE)
    create_expert_request(MINNIE_EMAIL, DONALD_EMAIL, MINNIE_MESSAGE)
    remove_client(DONALD_EMAIL, MINNIE_EMAIL)
    db = Database().get_session()
    messages = db.query(models.Message).filter(models.Message.cybersecurity_expert == DONALD_EMAIL).all()
    assert(len(messages) == 1)
    assert(MICKEY_EMAIL == messages[0].website_owner)
    
def test_delete_specialty_table():
    db_session = Database().get_session()  
    add_mock_specialty(db_session, DONALD_EMAIL, SQLI_NAME)
    add_vulnerability(db_session, XSS_NAME, XSS_DATE_ADDED)
    add_specialty(db_session, DONALD_EMAIL, XSS_NAME)
    assert (check_specialty(db_session, DONALD_EMAIL, SQLI_NAME) == True)
    assert (check_specialty(db_session, DONALD_EMAIL, XSS_NAME) == True)
    assert (delete_specialty(db_session, DONALD_EMAIL, XSS_NAME) == True)
    assert (check_specialty(db_session, DONALD_EMAIL, SQLI_NAME) == True)
    assert (check_specialty(db_session, DONALD_EMAIL, XSS_NAME) == False)
    assert (delete_specialty(db_session, DONALD_EMAIL, SQLI_NAME) == True)
    assert (check_specialty(db_session, DONALD_EMAIL, SQLI_NAME) == False)
    db_session.rollback()
    
def test_update_expert_info():
    populate_vulnerabilities()
    create_expert_account(DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME)
    create_website_owner(MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE)
    create_website_owner(MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE)
    create_expert_request(MICKEY_EMAIL, DONALD_EMAIL, MICKEY_MESSAGE)
    create_expert_request(MINNIE_EMAIL, DONALD_EMAIL, MINNIE_MESSAGE)
    add_expert_info(DONALD_EMAIL, DONALD_IMAGE, True, True, False, False)
    
    assert(update_expert_info(DONALD_EMAIL, DAISY_IMAGE, DAISY_PASSWORD, False, False, True, True) == True)
    assert(get_expert_info(DONALD_EMAIL)["image"] == DAISY_IMAGE
           and get_expert_info(DONALD_EMAIL)["password"] == DAISY_PASSWORD
           and get_expert_info(DONALD_EMAIL)["specialties"] == [NMAP_NAME, JWT_COOKIE_HIJACKING_NAME])
    
    assert(update_expert_info(DONALD_EMAIL, DAISY_IMAGE, DAISY_PASSWORD, False, False, True, True) == True)
    assert(get_expert_info(DONALD_EMAIL)["image"] == DAISY_IMAGE
           and get_expert_info(DONALD_EMAIL)["password"] == DAISY_PASSWORD
           and get_expert_info(DONALD_EMAIL)["specialties"] == [NMAP_NAME, JWT_COOKIE_HIJACKING_NAME])
    
    assert(update_expert_info(DONALD_EMAIL, DONALD_IMAGE, DONALD_PASSWORD, False, False, False, False) == True)

    assert(update_expert_info(DONALD_EMAIL, image=DAISY_IMAGE, password=None, sql=None, xss=None, nmap=None, jwt=None) == True)
    assert(get_expert_info(DONALD_EMAIL)["image"] == DAISY_IMAGE)
    
    assert(update_expert_info(DONALD_EMAIL, image=None, password=DAISY_PASSWORD, sql=None, xss=None, nmap=None, jwt=None) == True)
    assert(get_expert_info(DONALD_EMAIL)["password"] == DAISY_PASSWORD)

    assert(update_expert_info(DONALD_EMAIL, image=None, password=None, sql=True, xss=None, nmap=None, jwt=None) == True)
    assert(get_expert_info(DONALD_EMAIL)["specialties"] == [SQL_INJECTION_NAME])
    
    assert(update_expert_info(DONALD_EMAIL, image=None, password=None, sql=None, xss=True, nmap=None, jwt=None) == True)
    assert(get_expert_info(DONALD_EMAIL)["specialties"] == [SQL_INJECTION_NAME, XSS_NAME])
    
    assert(update_expert_info(DONALD_EMAIL, image=None, password=None, sql=None, xss=None, nmap=True, jwt=None) == True)
    assert(get_expert_info(DONALD_EMAIL)["specialties"] == [SQL_INJECTION_NAME, XSS_NAME, NMAP_NAME])
    
    assert(update_expert_info(DONALD_EMAIL, image=None, password=None, sql=None, xss=None, nmap=None, jwt=True) == True)
    assert(get_expert_info(DONALD_EMAIL)["specialties"] == [SQL_INJECTION_NAME, XSS_NAME, NMAP_NAME, JWT_COOKIE_HIJACKING_NAME])