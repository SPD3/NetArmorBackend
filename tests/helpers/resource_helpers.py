from src.resource_functions import add_resource
from src.vulnerability_functions import add_vulnerability
from tests.constants import SQLI_TITLE, SQLI_NAME, SQLI_DATE_ADDED, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE
from src.website_functions import add_website_owner

def add_mock_resource(db_session, link, title, vulnerability, date_added=SQLI_DATE_ADDED):
    add_vulnerability(db_session, vulnerability, date_added)
    add_resource(db_session, link, title, vulnerability)