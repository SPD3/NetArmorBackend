from src.expert_functions import check_cybersecurity_expert, add_cybersecurity_expert, check_cybersecurity_expert_rating, add_cybersecurity_expert_rating, check_specialty, add_specialty
from tests.constants import DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE, DONALD_RATING, SQLI_NAME, MICKEY_EMAIL

def check_donald(db_session):
    return check_cybersecurity_expert(db_session, DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE)

def add_donald(db_session):
    add_cybersecurity_expert(db_session, DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE)

def check_donald_rating(db_session):
    return check_cybersecurity_expert_rating(db_session, MICKEY_EMAIL, DONALD_EMAIL, DONALD_RATING)

def add_donald_rating(db_session):
    add_cybersecurity_expert_rating(db_session, MICKEY_EMAIL, DONALD_EMAIL, DONALD_RATING)
'''    
def add_mock_rating(db_session, website_owner, cybersecurity_expert, rating):
    add_cybersecurity_expert_rating(db_session, website_owner, cybersecurity_expert, rating)
'''
    
def check_donald_specialty(db_session):
    return check_specialty(db_session, DONALD_EMAIL, SQLI_NAME)

def add_donald_specialty(db_session):
    add_specialty(db_session, DONALD_EMAIL, SQLI_NAME)