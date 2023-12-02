from datetime import date
from src.vulnerability_functions import add_vulnerability

def populate_vulnerabilities(db_session):
    add_vulnerability(db_session, "SQL Injection", date.today())
    add_vulnerability(db_session, "Cross-Site Scripting", date.today())
    add_vulnerability(db_session, "NMAP", date.today())
    add_vulnerability(db_session, "JWT Cookie Hijacking", date.today())
    
def populate_tables(db_session):
    populate_vulnerabilities(db_session)
    