from src.certificate_functions import add_issued_certification
from tests.constants import DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE
from src.expert_functions import add_cybersecurity_expert

def add_mock_issued_certification(db_session, cert_image, email, password=DONALD_PASSWORD, first_name=DONALD_FIRST_NAME, last_name=DONALD_LAST_NAME, expert_image=DONALD_IMAGE):
    add_cybersecurity_expert(db_session, email, password, first_name, last_name, expert_image)
    add_issued_certification(db_session, cert_image, email)