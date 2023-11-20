from src.certificate_functions import add_certification, add_issued_certification
from tests.constants import PENTEST_LAUNCH_DATE, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE
from src.expert_functions import add_cybersecurity_expert

def add_mock_issued_certification(db_session, certification_number, certification_name, issuer, email, certification_issue_date, certification_launch_date=PENTEST_LAUNCH_DATE, password=DONALD_PASSWORD, first_name=DONALD_FIRST_NAME, last_name=DONALD_LAST_NAME, image=DONALD_IMAGE):
    add_certification(db_session, certification_name, issuer, certification_launch_date)
    add_cybersecurity_expert(db_session, email, password, first_name, last_name, image)
    add_issued_certification(db_session, certification_number, certification_name, issuer, email, certification_issue_date)