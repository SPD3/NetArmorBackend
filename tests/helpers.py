from src.table_functions import *
from tests.constants import *

def add_website_owners(db_session):
    add_mickey(db_session)
    add_website_owner(db_session, MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME)

def add_vulnerabilities(db_session):
    add_sqli_vulnerability(db_session)
    add_vulnerability(db_session, CSRF_NAME, CSRF_DATE_ADDED)
    
def add_websites(db_session):
    add_website_owners(db_session)
    add_mickey_website(db_session)
    add_website(db_session, MINNIE_URL, MINNIE_EMAIL, MINNIE_WEBSITE_NAME)
    
def add_cybersecurity_experts(db_session):
    add_donald(db_session)
    add_cybersecurity_expert(db_session, DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME) 
