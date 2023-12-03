import base64
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
from src import expert_endpoints

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
    try:
        with open("images/sean_profile_picture.png", "rb") as image:
            return base64.b64encode(image.read())
    except:
        return ""

def populate_sample_cybersecurity_experts():
    sean_email = "spd7416@nyu.edu"
    
    expert_endpoints.create_expert_account(sean_email, "seanpassword", "Sean", "Doyle")
    expert_endpoints.add_expert_info(sean_email, get_image_str("images/sean_profile_picture"), True, True, False, False)


def populate_sample_website_owners():
    db_session = Database().get_session()
    ... 

def populate_tables():
    if is_already_pre_populated():
        return
    populate_vulnerabilities()
    populate_sample_cybersecurity_experts()
    populate_sample_website_owners()



    