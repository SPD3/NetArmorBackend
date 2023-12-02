from .database import Database
from src.config import settings

from datetime import date
from src.vulnerability_functions import add_vulnerability

def create_vulnerability(vulnerability, date_added):
    db_session = Database().get_session()
    add_vulnerability(db_session, vulnerability, date_added)
    db_session.commit()
    return True

def populate_vulnerabilities():
    create_vulnerability("SQL Injection", date.today())
    create_vulnerability("Cross-Site Scripting", date.today())
    create_vulnerability("NMAP", date.today())
    create_vulnerability("JWT Cookie Hijacking", date.today())
    
def populate_tables():
    populate_vulnerabilities()
    