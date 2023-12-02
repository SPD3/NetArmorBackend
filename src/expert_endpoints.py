from . import crud, expert_functions
from .database import Database
from src.config import settings
from tg.util import Bunch

from src.netarmor_api import App, Endpoint
from src.expert_functions import add_specialty
from src.vulnerability_functions import add_vulnerability

def check_expert_info(email, password):
    db_session = Database().get_session()
    db_user = crud.get_expert_by_email(db_session, email=email)
    if db_user is None:
        return False
    return db_user.password == password

def expert_exists(email):
    db_session = Database().get_session()
    db_user = crud.get_expert_by_email(db_session, email=email)
    return db_user is not None

def create_expert_account(email, password, first_name, last_name):
    db_session = Database().get_session()
    db_user = crud.get_expert_by_email(db_session, email)
    if db_user:
        return False
    expert_functions.add_cybersecurity_expert(db_session, email, password, first_name, last_name)
    db_session.commit()
    return True

def delete_expert(email):
    db_session = Database().get_session()
    db_user = crud.get_expert_by_email(db_session, email)
    if not db_user:
        return False
    db_session.delete(db_user)
    db_session.commit()
    return True

def add_expert_info(email, image, sql, xss, nmap, jwt):
    db_session = Database().get_session()
    db_user = crud.get_expert_by_email(db_session, email=email)
    if db_user is None:
        return False
    db_user.image = image
    if sql:
        add_specialty(db_session, email, "SQL Injection")
    if xss:
        add_specialty(db_session, email, "Cross-Site Scripting")
    if nmap:
        add_specialty(db_session, email, "NMAP")
    if jwt:
        add_specialty(db_session, email, "JWT Cookie Hijacking")
    db_session.commit()
    return True