import base64
import datetime
from .database import Database
from src.config import settings

from datetime import date
from src.vulnerability_functions import add_vulnerability

from src.database import Database
from src.models import Base
from src.config import get_settings
from sqlalchemy import event
import contextlib
from src.models import Base
from src.website_functions import add_website_owner
from src.expert_functions import add_cybersecurity_expert, add_specialty
from src.certificate_functions import add_issued_certification
from src.website_functions import add_website
from src.scan_functions import add_scan
from src.vulnerability_functions import add_tested_vulnerability

SQL_INJECTION_NAME = "SQL Injection"
XSS_NAME = "Cross-Site Scripting"
NMAP_NAME = "NMAP"
JWT_COOKIE_HIJACKING_NAME = "JWT Cookie Hijacking"

def create_vulnerability(vulnerability, date_added):
    db_session = Database().get_session()
    add_vulnerability(db_session, vulnerability, date_added)
    db_session.commit()
    return True

def populate_vulnerabilities():
    create_vulnerability(SQL_INJECTION_NAME, date.today())
    create_vulnerability(XSS_NAME, date.today())
    create_vulnerability(NMAP_NAME, date.today())
    create_vulnerability(JWT_COOKIE_HIJACKING_NAME, date.today())
    
def is_already_pre_populated():
    """Checks to see if any of the tables already have entries in them."""
    tables = Base.__subclasses__()
    db_session = Database().get_session()
    for t in tables:
        if len(db_session.query(t).all()) != 0:
            return True
    
    return False

def get_image_str(image_location:str):
    prefix = "data:image/png;base64,"
    try:
        with open(image_location, "rb") as image:
            encoding = base64.b64encode(image.read())
            encoding = str(encoding)[2:-1] # first two characters are b', last character is '
            return prefix + encoding
    except:
        return ""

def populate_sample_data():
    print("POPULATING SAMPLE DATA")
    sean_email = "spd7416@nyu.edu"
    andrew_email = "at4704@nyu.edu"
    jimmy_email = "js11718@nyu.edu"
    mitchell_email = "mz2909@nyu.edu"
    db_session = Database().get_session()
    url = "https://jiminator.github.io/Midterm/"
    add_website_owner(db_session, sean_email, "seanpassword", "Sean", "Doyle", get_image_str("images/sean_profile_picture.png"))
    add_website(db_session=db_session, url=url, owner_email=sean_email, website_name=url)
    scan_id = add_scan(db_session=db_session, owner_email=sean_email, url=url, deep=False, date=datetime.datetime.now())
    add_tested_vulnerability(db_session, scan_id, SQL_INJECTION_NAME, 100, True, "All good")
    add_tested_vulnerability(db_session, scan_id, XSS_NAME, 100, True, "All good")
    add_tested_vulnerability(db_session, scan_id, NMAP_NAME, 0, True, "Fail")


    add_cybersecurity_expert(db_session, andrew_email, "andrewpassword", "Andrew", "Tang", get_image_str("images/andrew_profile_picture.png"))
    add_specialty(db_session, andrew_email, SQL_INJECTION_NAME)
    add_specialty(db_session, andrew_email, XSS_NAME)
    add_issued_certification(db_session, get_image_str("images/andrew_cert_1.png"), andrew_email)
    add_issued_certification(db_session, get_image_str("images/andrew_cert_2.png"), andrew_email)
    add_cybersecurity_expert(db_session, jimmy_email, "jimmypassword", "Jimmy", "Shong", get_image_str("images/jimmy_profile_picture.png"))
    add_specialty(db_session, jimmy_email, NMAP_NAME)
    add_specialty(db_session, jimmy_email, XSS_NAME)
    add_cybersecurity_expert(db_session, mitchell_email, "mitchellpassword", "Mitchell", "Zhou", get_image_str("images/mitchell_profile_picture.png"))
    add_specialty(db_session, mitchell_email, NMAP_NAME)
    add_specialty(db_session, mitchell_email, JWT_COOKIE_HIJACKING_NAME)
    add_specialty(db_session, mitchell_email, SQL_INJECTION_NAME)
    add_issued_certification(db_session, get_image_str("images/mitchell_cert_1.png"), mitchell_email)
    db_session.commit()
    print("DONE POPULATING SAMPLE DATA")

def populate_tables():
    if is_already_pre_populated():
        return
    populate_vulnerabilities()
    populate_sample_data()



    