from tests.test_main import *


def test_add_certificate_table():
    db_session = Database().get_session()    
    generic_add_test(lambda: check_pentest_certification(db_session), 
                     lambda: add_pentest_certification(db_session), 
                     lambda: check_certification(db_session, CLOUD_CERTIFICATION_NAME, CLOUD_ISSUER, CLOUD_LAUNCH_DATE),
                     lambda: add_certification(db_session, CLOUD_CERTIFICATION_NAME, CLOUD_ISSUER, CLOUD_LAUNCH_DATE))
    db_session.rollback()
    
def test_duplicate_certificate_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, lambda: add_pentest_certification(db_session))
    db_session.rollback()
    
def test_add_issued_certification_table():
    db_session = Database().get_session()
    add_pentest_certification(db_session)
    add_certification(db_session, CLOUD_CERTIFICATION_NAME, CLOUD_ISSUER, CLOUD_LAUNCH_DATE)
    add_cybersecurity_experts(db_session)  
    generic_add_test(lambda: check_issued_pentest_certification(db_session), 
                     lambda: add_issued_pentest_certification(db_session), 
                     lambda: check_issued_certification(db_session, CLOUD_CERTIFICATION_NUMBER, CLOUD_CERTIFICATION_NAME, CLOUD_ISSUER, DAISY_EMAIL, CLOUD_DATE_ISSUED),
                     lambda: add_issued_certification(db_session, CLOUD_CERTIFICATION_NUMBER, CLOUD_CERTIFICATION_NAME, CLOUD_ISSUER, DAISY_EMAIL, CLOUD_DATE_ISSUED))
    db_session.rollback()

def test_duplicate_issued_certification_table():
    db_session = Database().get_session()
    add_pentest_certification(db_session)
    add_donald(db_session)
    generic_duplicate_test(db_session, 
                lambda: add_issued_pentest_certification(db_session))
    db_session.rollback()