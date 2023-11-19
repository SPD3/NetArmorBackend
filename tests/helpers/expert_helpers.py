from src.expert_functions import add_cybersecurity_expert, add_cybersecurity_expert_rating, add_specialty
from src.website_functions import add_website_owner
from src.vulnerability_functions import add_vulnerability
from tests.constants import DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE, SQLI_DATE

def add_mock_expert_rating(db_session, website_owner, expert, rating, owner_password=MICKEY_PASSWORD, owner_first_name=MICKEY_FIRST_NAME, owner_last_name=MICKEY_LAST_NAME, owner_image=MICKEY_IMAGE, expert_password=DONALD_PASSWORD, expert_first_name=DONALD_FIRST_NAME, expert_last_name=DONALD_LAST_NAME, expert_image=DONALD_IMAGE):
    add_website_owner(db_session, website_owner, owner_password, owner_first_name, owner_last_name, owner_image)
    add_cybersecurity_expert(db_session, expert, expert_password, expert_first_name, expert_last_name, expert_image)
    add_cybersecurity_expert_rating(db_session, website_owner, expert, rating)

def add_mock_specialty(db_session, email, vulnerability, expert_password=DONALD_PASSWORD, expert_first_name=DONALD_FIRST_NAME, expert_last_name=DONALD_LAST_NAME, expert_image=DONALD_IMAGE, vulnerability_date_added=SQLI_DATE):
    add_cybersecurity_expert(db_session, email, expert_password, expert_first_name, expert_last_name, expert_image)
    add_vulnerability(db_session, vulnerability, vulnerability_date_added)
    add_specialty(db_session, email, vulnerability)