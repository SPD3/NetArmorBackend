from src.website_functions import add_website, add_website_owner
from src.vulnerability_functions import add_vulnerability
from tests.helpers.vulnerability_helpers import add_sqli_vulnerability
from src.expert_functions import add_cybersecurity_expert
from tests.helpers.website_helpers import add_mickey_website, add_mickey
from tests.helpers.expert_helpers import add_donald
from tests.constants import MINNIE_IMAGE, MINNIE_EMAIL, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_PASSWORD, MINNIE_URL, MINNIE_WEBSITE_NAME, CSRF_DATE_ADDED, CSRF_NAME, DAISY_EMAIL, DAISY_FIRST_NAME, DAISY_LAST_NAME, DAISY_PASSWORD, DAISY_IMAGE

def add_website_owners(db_session):
    add_mickey(db_session)
    add_website_owner(db_session, MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE)
    
def add_websites(db_session):
    add_website_owners(db_session)
    add_mickey_website(db_session)
    add_website(db_session, MINNIE_URL, MINNIE_EMAIL, MINNIE_WEBSITE_NAME)

def add_vulnerabilities(db_session):
    add_sqli_vulnerability(db_session)
    add_vulnerability(db_session, CSRF_NAME, CSRF_DATE_ADDED)
    
def add_cybersecurity_experts(db_session):
    add_donald(db_session)
    add_cybersecurity_expert(db_session, DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME, DAISY_IMAGE) 
