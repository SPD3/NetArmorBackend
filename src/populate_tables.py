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
def populate_tables():
    if is_already_pre_populated():
        return
    populate_vulnerabilities()


    