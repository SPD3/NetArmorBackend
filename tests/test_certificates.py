from src.database import Database
from tests.constants import DAISY_EMAIL, DONALD_EMAIL, PENTEST_IMAGE, CLOUD_IMAGE
from tests.test_main import generic_add_test, generic_duplicate_test
from src.certificate_functions import check_issued_certification, add_issued_certification
from tests.helpers.certificate_helpers import add_mock_issued_certification
    
def test_add_issued_certification_table():
    db_session = Database().get_session()  
    generic_add_test(lambda: check_issued_certification(db_session, PENTEST_IMAGE, DONALD_EMAIL), 
                     lambda: add_mock_issued_certification(db_session, PENTEST_IMAGE, DONALD_EMAIL), 
                     lambda: check_issued_certification(db_session, CLOUD_IMAGE, DAISY_EMAIL),
                     lambda: add_mock_issued_certification(db_session, CLOUD_IMAGE, DAISY_EMAIL))
    db_session.rollback()

def test_duplicate_issued_certification_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                lambda: add_mock_issued_certification(db_session, PENTEST_IMAGE, DONALD_EMAIL), 
                lambda: add_issued_certification(db_session, PENTEST_IMAGE, DONALD_EMAIL))
    db_session.rollback()