from src.certificate_functions import check_certification, add_certification, check_issued_certification, add_issued_certification
from tests.constants import PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, PENTEST_LAUNCH_DATE, PENTEST_DATE_ISSUED, DONALD_EMAIL

def check_pentest_certification(db_session):
    return check_certification(db_session, PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, PENTEST_LAUNCH_DATE)

def add_pentest_certification(db_session):
    add_certification(db_session, PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, PENTEST_LAUNCH_DATE)
    
def check_issued_pentest_certification(db_session):
    return check_issued_certification(db_session, 12345, PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, DONALD_EMAIL, PENTEST_DATE_ISSUED)

def add_issued_pentest_certification(db_session):
    add_issued_certification(db_session, 12345, PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, DONALD_EMAIL, PENTEST_DATE_ISSUED)