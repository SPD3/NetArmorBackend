from src.resource_functions import check_resource, add_resource, check_resource_rating, add_resource_rating
from tests.constants import SQLI_LINK, SQLI_TITLE, SQLI_NAME, SQLI_RATING, MICKEY_EMAIL

def check_sqli_resource(db_session):
    return check_resource(db_session, SQLI_LINK, SQLI_TITLE, SQLI_NAME)

def add_sqli_resource(db_session):
    add_resource(db_session, SQLI_LINK, SQLI_TITLE, SQLI_NAME)
    
def check_sqli_rating(db_session):
    return check_resource_rating(db_session, MICKEY_EMAIL, SQLI_LINK, SQLI_RATING)

def add_sqli_rating(db_session):
    add_resource_rating(db_session, MICKEY_EMAIL, SQLI_LINK, SQLI_RATING)