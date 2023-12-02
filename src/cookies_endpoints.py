import random
import string
from .database import Database
from .website_functions import check_cookie_exists, add_or_update_cookie_entry, get_email_from_cookie_and_is_website_owner, delete_cookie_if_it_exists

COOKIE_LENGTH = 15
COOKIE_CHARS = string.ascii_letters
COOKIE_RETRIES = 10

def create_cookie(email:str, is_website_owner:bool):
    db_session = Database().get_session()
    for i in range(COOKIE_RETRIES):
        cookie = ''.join(random.choices(COOKIE_CHARS, k=COOKIE_LENGTH))
        if not check_cookie_exists(db_session, cookie):
            break
    if i >= COOKIE_RETRIES:
        return None
    add_or_update_cookie_entry(db_session, cookie, is_website_owner, email)
    try:
        db_session.commit()
    except Exception as e:
        print(e)
        db_session.rollback()
        return None

    return cookie

def validate_cookie(cookie:str, is_website_owner:bool):
    db_session = Database().get_session()
    return get_email_from_cookie_and_is_website_owner(db_session, cookie, is_website_owner)

def delete_cookie(cookie:str):
    db_session = Database().get_session()
    delete_cookie_if_it_exists(db_session, cookie)
    db_session.commit()
    
