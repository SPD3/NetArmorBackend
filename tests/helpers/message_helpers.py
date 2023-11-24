from src.expert_functions import add_cybersecurity_expert
from src.website_functions import add_website_owner
from src.message_functions import add_message
from tests.constants import DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE

def add_mock_message(db_session, website_owner, expert, payload, status, time_sent, owner_password=MICKEY_PASSWORD, owner_first_name=MICKEY_FIRST_NAME, owner_last_name=MICKEY_LAST_NAME, owner_image=MICKEY_IMAGE, expert_password=DONALD_PASSWORD, expert_first_name=DONALD_FIRST_NAME, expert_last_name=DONALD_LAST_NAME, expert_image=DONALD_IMAGE):
    add_website_owner(db_session, website_owner, owner_password, owner_first_name, owner_last_name, owner_image)
    add_cybersecurity_expert(db_session, expert, expert_password, expert_first_name, expert_last_name, expert_image)
    add_message(db_session, website_owner, expert, payload, status, time_sent)