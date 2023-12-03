from . import crud, expert_functions
from .database import Database
from src.config import settings
from tg.util import Bunch

from src.netarmor_api import App, Endpoint
from src.expert_functions import add_specialty
from src.populate_tables import SQL_INJECTION_NAME, XSS_NAME, NMAP_NAME, JWT_COOKIE_HIJACKING_NAME
from src.utils import convert_strings_to_bools

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
    params = [sql, xss, nmap, jwt]
    convert_strings_to_bools(params)
    if params[0]:
        add_specialty(db_session, email, SQL_INJECTION_NAME)
    if params[1]:
        add_specialty(db_session, email, XSS_NAME)
    if params[2]:
        add_specialty(db_session, email, NMAP_NAME)
    if params[3]:
        add_specialty(db_session, email, JWT_COOKIE_HIJACKING_NAME)
    db_session.commit()
    return True

def get_expert_info(email):
    db_session = Database().get_session()
    db_user = crud.get_expert_by_email(db_session, email=email)
    if db_user is None:
        return False
    result = {}
    result["email"] = db_user.email
    result["password"] = db_user.password
    result["first_name"] = db_user.first_name
    result["last_name"] = db_user.last_name
    result["image"] = db_user.image
    
    certifications_list = []
    for certification in db_user.certifications:
        certifications_list.append(certification.image)
    result["certifications"] = certifications_list
    
    specialties_list = []
    for specialty in db_user.specialty:
        specialties_list.append(specialty.vulnerability)
    result["specialties"] = specialties_list
    
    client_list = []
    for message in db_user.messages:
        client_list.append(message.website_owner)
    result["clients"] = client_list
    return result