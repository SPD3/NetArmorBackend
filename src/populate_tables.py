from .database import Database
from src.config import settings

from datetime import date
from src.vulnerability_functions import add_vulnerability

from src.database import Database
from src.models import Base
from src.config import get_settings
import contextlib

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
    meta = Base.metadata
    with contextlib.closing(Database().get_engine().connect()) as con:
        trans = con.begin()
        tables = meta.sorted_tables
        for table in reversed(tables):
            con.execute(table.delete())
        trans.commit()

    populate_vulnerabilities()
    