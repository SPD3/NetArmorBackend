from src.database import Database
from tests.constants import CLOUD_CERTIFICATION_NAME, CLOUD_ISSUER, CLOUD_LAUNCH_DATE, CLOUD_CERTIFICATION_NUMBER, DAISY_EMAIL, CLOUD_DATE_ISSUED, PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, PENTEST_CERTIFICATION_NUMBER, DONALD_EMAIL, PENTEST_LAUNCH_DATE, PENTEST_DATE_ISSUED
from tests.test_main import generic_add_test, generic_duplicate_test
from src.certificate_functions import check_certification, add_certification, check_issued_certification, add_issued_certification
from tests.helpers.certificate_helpers import add_mock_issued_certification

def test_add_certificate_table():
    db_session = Database().get_session()    
    generic_add_test(lambda: check_certification(db_session, PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, PENTEST_LAUNCH_DATE), 
                     lambda: add_certification(db_session, PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, PENTEST_LAUNCH_DATE), 
                     lambda: check_certification(db_session, CLOUD_CERTIFICATION_NAME, CLOUD_ISSUER, CLOUD_LAUNCH_DATE),
                     lambda: add_certification(db_session, CLOUD_CERTIFICATION_NAME, CLOUD_ISSUER, CLOUD_LAUNCH_DATE))
    db_session.rollback()
    
def test_duplicate_certificate_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                           lambda: add_certification(db_session, PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, PENTEST_LAUNCH_DATE),
                           lambda: add_certification(db_session, PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, CLOUD_LAUNCH_DATE))
    db_session.rollback()
    
def test_add_issued_certification_table():
    db_session = Database().get_session()  
    generic_add_test(lambda: check_issued_certification(db_session, PENTEST_CERTIFICATION_NUMBER, PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, DONALD_EMAIL, PENTEST_DATE_ISSUED), 
                     lambda: add_mock_issued_certification(db_session, PENTEST_CERTIFICATION_NUMBER, PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, DONALD_EMAIL, PENTEST_DATE_ISSUED), 
                     lambda: check_issued_certification(db_session, CLOUD_CERTIFICATION_NUMBER, CLOUD_CERTIFICATION_NAME, CLOUD_ISSUER, DAISY_EMAIL, CLOUD_DATE_ISSUED),
                     lambda: add_mock_issued_certification(db_session, CLOUD_CERTIFICATION_NUMBER, CLOUD_CERTIFICATION_NAME, CLOUD_ISSUER, DAISY_EMAIL, CLOUD_DATE_ISSUED))
    db_session.rollback()

def test_duplicate_issued_certification_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                lambda: add_mock_issued_certification(db_session, PENTEST_CERTIFICATION_NUMBER, PENTEST_CERTIFICATION_NAME, PENTEST_ISSUER, DONALD_EMAIL, PENTEST_DATE_ISSUED), 
                lambda: add_issued_certification(db_session, PENTEST_CERTIFICATION_NUMBER, PENTEST_CERTIFICATION_NAME, CLOUD_ISSUER, DAISY_EMAIL, CLOUD_DATE_ISSUED))
    db_session.rollback()