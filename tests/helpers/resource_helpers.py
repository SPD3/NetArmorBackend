from src.resource_functions import add_resource, add_resource_rating
from src.vulnerability_functions import add_vulnerability
from tests.constants import SQLI_TITLE, SQLI_NAME, SQLI_DATE, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE, SQLI_DESCRIPTION
from src.website_functions import add_website_owner

def add_mock_resource(db_session, link, title, vulnerability, description=SQLI_DESCRIPTION, date_added=SQLI_DATE):
    add_vulnerability(db_session, vulnerability, description, date_added)
    add_resource(db_session, link, title, vulnerability)

def add_mock_resource_rating(db_session, email, link, rating, vulnerability=SQLI_NAME, password=MICKEY_PASSWORD, first_name=MICKEY_FIRST_NAME, last_name=MICKEY_LAST_NAME, image=MICKEY_IMAGE, title=SQLI_TITLE):
    add_website_owner(db_session, email, password, first_name, last_name, image)
    add_mock_resource(db_session, link, title, vulnerability)
    add_resource_rating(db_session, email, link, rating)