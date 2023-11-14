from src.website_functions import check_website_owner, add_website_owner, check_website, add_website
from tests.constants import MICKEY_URL, MICKEY_EMAIL, MICKEY_WEBSITE_NAME, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE


def check_mickey_website(db_session):
    return check_website(db_session, MICKEY_URL, MICKEY_EMAIL, MICKEY_WEBSITE_NAME)

def add_mickey_website(db_session):
    add_website(db_session, MICKEY_URL, MICKEY_EMAIL, MICKEY_WEBSITE_NAME)
    
def check_mickey(db_session):
    return check_website_owner(db_session, MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE)

def add_mickey(db_session):
    add_website_owner(db_session, MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE)