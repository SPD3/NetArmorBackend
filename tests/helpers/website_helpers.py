from src.website_functions import add_website_owner, add_website
from tests.constants import MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE

def add_mock_website(db_session, url, email, website_name, password=MICKEY_PASSWORD, first_name=MICKEY_FIRST_NAME, last_name=MICKEY_LAST_NAME, image=MICKEY_IMAGE):
    add_website_owner(db_session, email, password, first_name, last_name, image)
    add_website(db_session, url, email, website_name)