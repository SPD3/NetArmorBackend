from src.database import Database
from tests.constants import CSRF_RESOURCE_URL, CSRF_TITLE, CSRF_NAME, MINNIE_EMAIL, CSRF_RATING
from tests.test_main import generic_add_test, generic_duplicate_test
from src.resource_functions import check_resource, add_resource, check_resource_rating, add_resource_rating
from tests.helpers.vulnerability_helpers import add_sqli_vulnerability
from tests.helpers.helper import add_vulnerabilities, add_website_owners
from tests.helpers.website_helpers import add_mickey
from tests.helpers.resource_helpers import check_sqli_resource, add_sqli_resource, check_sqli_rating, add_sqli_rating


def test_add_resource_table():
    db_session = Database().get_session()
    add_vulnerabilities(db_session)
    generic_add_test(lambda: check_sqli_resource(db_session), 
                     lambda: add_sqli_resource(db_session), 
                     lambda: check_resource(db_session, CSRF_RESOURCE_URL, CSRF_TITLE, CSRF_NAME),
                     lambda: add_resource(db_session, CSRF_RESOURCE_URL, CSRF_TITLE, CSRF_NAME))
    db_session.rollback()

def test_duplicate_resource_table():
    db_session = Database().get_session()
    add_sqli_vulnerability(db_session)
    generic_duplicate_test(db_session, lambda: add_sqli_resource(db_session))
    db_session.rollback()

def test_add_resource_rating():
    db_session = Database().get_session()
    add_website_owners(db_session)
    add_vulnerabilities(db_session)
    add_sqli_resource(db_session)
    add_resource(db_session, CSRF_RESOURCE_URL, CSRF_TITLE, CSRF_NAME)
    generic_add_test(lambda: check_sqli_rating(db_session), 
                     lambda: add_sqli_rating(db_session), 
                     lambda: check_resource_rating(db_session, MINNIE_EMAIL, CSRF_RESOURCE_URL, CSRF_RATING),
                     lambda: add_resource_rating(db_session, MINNIE_EMAIL, CSRF_RESOURCE_URL, CSRF_RATING))
    db_session.rollback()

def test_duplicate_resource_rating():
    db_session = Database().get_session()
    add_mickey(db_session)
    add_sqli_vulnerability(db_session)
    add_sqli_resource(db_session)
    generic_duplicate_test(db_session, lambda: add_sqli_rating(db_session))
    db_session.rollback()