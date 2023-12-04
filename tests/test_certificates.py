from src.database import Database
from tests.constants import DAISY_EMAIL, DONALD_EMAIL, PENTEST_IMAGE, CLOUD_IMAGE, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE
from tests.test_main import generic_add_test, generic_duplicate_test
from src.certificate_functions import check_issued_certification, add_issued_certification
from tests.helpers.certificate_helpers import add_mock_issued_certification
from src.certificate_endpoints import remove_cert, add_cert
from src.expert_endpoints import create_expert_account
from src import crud
    
def test_add_issued_certification_table():
    db_session = Database().get_session()  
    generic_add_test(lambda: check_issued_certification(db_session, PENTEST_IMAGE, DONALD_EMAIL), 
                     lambda: add_mock_issued_certification(db_session, PENTEST_IMAGE, DONALD_EMAIL), 
                     lambda: check_issued_certification(db_session, CLOUD_IMAGE, DAISY_EMAIL),
                     lambda: add_mock_issued_certification(db_session, CLOUD_IMAGE, DAISY_EMAIL))
    db_session.rollback()
    
def test_add_cert():
    create_expert_account(DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME)
    add_cert(PENTEST_IMAGE, DONALD_EMAIL)
    add_cert(CLOUD_IMAGE, DONALD_EMAIL)
    db = Database().get_session()
    issued_certifications = crud.get_certifications(db)
    assert(len(issued_certifications) == 2)
    certification_set = set()
    for certification in issued_certifications:
        assert (certification.recipient == DONALD_EMAIL)
        certification_set.add(certification.image)
    assert (PENTEST_IMAGE in certification_set and CLOUD_IMAGE in certification_set)
    
def test_remove_cert():
    create_expert_account(DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME)
    add_cert(PENTEST_IMAGE, DONALD_EMAIL)
    add_cert(CLOUD_IMAGE, DONALD_EMAIL)
    remove_cert(DONALD_EMAIL, CLOUD_IMAGE)
    db = Database().get_session()
    issued_certifications = crud.get_certifications(db)
    assert(len(issued_certifications) == 1)
    assert(PENTEST_IMAGE == issued_certifications[0].image)