from src.scan_functions import add_scan
from tests.helpers.website_helpers import add_mock_website
from tests.constants import MICKEY_WEBSITE_NAME, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE

def add_mock_scan(db_session, email, url, deep, date_added, website_name=MICKEY_WEBSITE_NAME, password=MICKEY_PASSWORD, first_name=MICKEY_FIRST_NAME, last_name=MICKEY_LAST_NAME, image=MICKEY_IMAGE):
    add_mock_website(db_session, url, email, website_name, password, first_name, last_name, image)
    add_scan(db_session, email, url, deep, date_added)