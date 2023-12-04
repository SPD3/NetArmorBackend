from . import crud, expert_functions
from .database import Database
from src.config import settings
from tg.util import Bunch

from src.netarmor_api import App, Endpoint
from src.expert_functions import add_specialty, delete_specialty
from src.populate_tables import SQL_INJECTION_NAME, XSS_NAME, NMAP_NAME, JWT_COOKIE_HIJACKING_NAME
from src.utils import convert_string_to_bool
from typing import Union
from src import models

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
        add_specialty(db_session, email, SQL_INJECTION_NAME)
    if xss:
        add_specialty(db_session, email, XSS_NAME)
    if nmap:
        add_specialty(db_session, email, NMAP_NAME)
    if jwt:
        add_specialty(db_session, email, JWT_COOKIE_HIJACKING_NAME)
    db_session.commit()
    return True


def get_certifications_for_db_user(db_user):
    certifications_list = []
    for certification in db_user.certifications:
        certifications_list.append(certification.image)
    return certifications_list
    
def get_specialties_for_db_user(db_user):
    specialties_list = []
    for specialty in db_user.specialty:
        specialties_list.append(specialty.vulnerability)
    
    return specialties_list

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
    result["certifications"] = get_certifications_for_db_user(db_user)
    result["specialties"] = get_specialties_for_db_user(db_user)
    
    client_list = []
    for message in db_user.messages:
        client_list.append({"email":message.website_owner, "message":message.payload})
    result["clients"] = client_list
    return result

def remove_client(expert_email, owner_email):
    db_session = Database().get_session()
    db_user = crud.get_expert_by_email(db_session, email=expert_email)
    if db_user is None:
        return False
    db_message = crud.get_message_by_emails(db_session, expert_email, owner_email)
    db_session.delete(db_message)
    db_session.commit()
    return True

def update_expert_info(email:str, image:Union[str,None], password:Union[str,None], 
                       sql:Union[bool,None], xss:Union[bool,None], nmap:Union[bool,None], jwt:Union[bool,None]):
    db_session = Database().get_session()
    db_expert = db_session.query(models.CybersecurityExpert).filter(models.CybersecurityExpert.email==email).all()
    
    if len(db_expert) != 1:
        return None
    db_expert = db_expert[0]
    
    if image:
        db_expert.image = image
        
    if password:
        db_expert.password = password
        
    if sql == True:
        add_specialty(db_session, email, SQL_INJECTION_NAME)
    elif sql == False:
        delete_specialty(db_session, email, SQL_INJECTION_NAME)
        
    if xss == True:
        add_specialty(db_session, email, XSS_NAME)
    elif xss == False:
        delete_specialty(db_session, email, XSS_NAME)
        
    if nmap == True:
        add_specialty(db_session, email, NMAP_NAME)
    elif nmap == False:
        delete_specialty(db_session, email, NMAP_NAME)
        
    if jwt == True:
        add_specialty(db_session, email, JWT_COOKIE_HIJACKING_NAME)
    elif jwt == False:
        delete_specialty(db_session, email, JWT_COOKIE_HIJACKING_NAME)
        
    db_session.commit()
    return True