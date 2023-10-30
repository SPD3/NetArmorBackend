from unittest.mock import patch
import pytest
from src.main import basic_endpoint, create_account, account_exists
from src.database import Database
from src import models, schemas
from datetime import date
from tests.table_functions import *

def test_add_website_owner_table():
    db_session = Database().get_session()
    minnie_email = "minnie@mouse.com"
    minnie_password = "12346"
    generic_add_test(lambda: check_mickey(db_session), 
                     lambda: add_mickey(db_session), 
                     lambda: check_website_owner(db_session, minnie_email, minnie_password),
                     lambda: add_website_owner(db_session, minnie_email, minnie_password))
    db_session.rollback()

def test_duplicate_websiste_owner_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                    lambda: add_mickey(db_session))
    db_session.rollback()
    
def test_add_website_table():
    db_session = Database().get_session()
    minnie_website_url = "minniemousewebsite.com"
    minnie_email = "minnie@mouse.com"
    minnie_password = "12346"
    minnie_website_name = "Minnie's Website"
    generic_add_test(lambda: check_mickey_website(db_session), 
                     lambda: add_mickey_website(db_session), 
                     lambda: check_website(db_session, minnie_website_url, minnie_email, minnie_website_name),
                     lambda: add_website(db_session, minnie_website_url, minnie_email, minnie_password, minnie_website_name))
    db_session.rollback()

def test_duplicate_websiste_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                lambda: add_mickey_website(db_session))
    db_session.rollback()
    
def test_add_certificate_table():
    db_session = Database().get_session()    
    cloud_name="Cloud+"
    cloud_issuer="CompTIA"
    cloud_launch_date=date(2021, 6, 9)
    generic_add_test(lambda: check_pentest_certification(db_session), 
                     lambda: add_pentest_certification(db_session), 
                     lambda: check_certification(db_session, cloud_name, cloud_issuer, cloud_launch_date),
                     lambda: add_certification(db_session, cloud_name, cloud_issuer, cloud_launch_date))
    db_session.rollback()

def test_duplicate_certificate_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                    lambda: add_pentest_certification(db_session))
    db_session.rollback()
    
def test_add_vulnerability_table():
    db_session = Database().get_session()    
    csrf_name="Cross-Site Request Forgery"
    csrf_date_added=date.today()
    generic_add_test(lambda: check_sqli_vulnerability(db_session), 
                     lambda: add_sqli_vulnerability(db_session), 
                     lambda: check_vulnerability(db_session, csrf_name, csrf_date_added),
                     lambda: add_vulnerability(db_session, csrf_name, csrf_date_added))
    db_session.rollback()

def test_duplicate_vulnerability_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                    lambda: add_sqli_vulnerability(db_session))
    db_session.rollback()

def test_add_resource_table():
    db_session = Database().get_session()
    csrf_resource_url = "https://owasp.org/www-community/attacks/csrf"
    csrf_title = "Cross Site Request Forgery (CSRF)"
    csrf_vulnerability = "Cross-Site Request Forgery"
    csrf_date_added = date.today()
    generic_add_test(lambda: check_sqli_resource(db_session), 
                     lambda: add_sqli_resource(db_session), 
                     lambda: check_resource(db_session, csrf_resource_url, csrf_title, csrf_vulnerability),
                     lambda: add_resource(db_session, csrf_resource_url, csrf_title, csrf_vulnerability, csrf_date_added))
    db_session.rollback()

def test_duplicate_resource_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                lambda: add_sqli_resource(db_session))
    db_session.rollback()
    
def test_add_cybersecurity_expert_table():
    db_session = Database().get_session()
    daisy_email = "daisy@duck.com"
    daisy_password = "6789"
    daisy_first_name = "Daisy"
    daisy_last_name = "Duck"
    generic_add_test(lambda: check_donald(db_session), 
                     lambda: add_donald(db_session), 
                     lambda: check_cybersecurity_expert(db_session, daisy_email, daisy_password, daisy_first_name, daisy_last_name),
                     lambda: add_cybersecurity_expert(db_session, daisy_email, daisy_password, daisy_first_name, daisy_last_name))
    db_session.rollback()

def test_duplicate_cybersecurity_expert_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                lambda: add_donald(db_session))
    db_session.rollback()

def test_add_issued_certification_table():
    db_session = Database().get_session()
    cloud_certification_number = 6789
    cloud_certification_name="Cloud+"
    cloud_issuer="CompTIA"
    cloud_launch_date = date(2021, 6, 9)
    cloud_recipient = "daisy@duck.com"
    cloud_password = "6789"
    cloud_first_name = "Daisy"
    cloud_last_name = "Duck"
    cloud_date_issued = date.today()
    generic_add_test(lambda: check_issued_pentest_certification(db_session), 
                     lambda: add_issued_pentest_certification(db_session), 
                     lambda: check_issued_certification(db_session, cloud_certification_number, cloud_certification_name, cloud_issuer, cloud_recipient, cloud_date_issued),
                     lambda: add_issued_certification(db_session, cloud_certification_number, cloud_certification_name, cloud_issuer, cloud_launch_date,
                             cloud_recipient, cloud_password, cloud_first_name, cloud_last_name,
                             cloud_date_issued))
    db_session.rollback()

def test_duplicate_issued_certification_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                lambda: add_issued_pentest_certification(db_session))
    db_session.rollback()
    
def test_add_specialty_table():
    db_session = Database().get_session()
    daisy_email = "daisy@duck.com"
    daisy_password = "6789"
    daisy_first_name = "Daisy"
    daisy_last_name = "Duck"
    csrf_name="Cross-Site Request Forgery"
    csrf_date_added=date.today()

    
    generic_add_test(lambda: check_donald_specialty(db_session), 
                     lambda: add_donald_specialty(db_session), 
                     lambda: check_specialty(db_session, daisy_email, csrf_name),
                     lambda: add_specialty(db_session, daisy_email, daisy_password, daisy_first_name, daisy_last_name, csrf_name, csrf_date_added))
    db_session.rollback()

def test_duplicate_specialty_table():
    db_session = Database().get_session()
    generic_duplicate_test(db_session, 
                lambda: add_donald_specialty(db_session))
    db_session.rollback()