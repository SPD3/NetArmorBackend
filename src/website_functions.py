import datetime
from src import models

DAYS_COOKIE_IS_VALID = 3

# Website Owner Functions
def check_website_owner(db_session, email, password, first_name, last_name, image):
    website_owners = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email==email).all()
    if len(website_owners) != 1:
        return False
    website_owner =  website_owners[0]
    return  (website_owner.password == password
                                          and website_owner.first_name == first_name
                                          and website_owner.last_name == last_name
                                          and website_owner.image == image)
    
def add_website_owner(db_session, email, password, first_name, last_name, image):
    db_website = models.WebsiteOwner(email=email, password=password, first_name=first_name, last_name=last_name, image=image)
    db_session.add(db_website)
    

# Website Functions
def check_website(db_session, url, owner_email, website_name):
    websites = db_session.query(models.Website).filter(models.Website.url==url).all()
    if len(websites) != 1:
        return False
    website = websites[0]
    return website is not None and website.owner_email == owner_email and website.website_name == website_name

def add_website(db_session, url, owner_email, website_name):
    db_website = models.Website(url=url, owner_email=owner_email, website_name=website_name)
    db_session.add(db_website)

    
# Cookie Functions
def check_cookie_exists_for_email(db_session, cookie_value, email):
    cookies = db_session.query(models.Cookie).filter(models.Cookie.cookie_value==cookie_value).all()
    if len(cookies) != 1:
        return False
    cookie = cookies[0]
    return cookie is not None and cookie.email == email

def cookie_entry_exists(db_session, is_website_owner:bool, email:str):
    cookies = db_session.query(models.Cookie).filter(models.Cookie.is_website_owner==is_website_owner).filter(models.Cookie.email==email).all()
    return len(cookies) == 1

def update_cookie_entry(db_session, cookie_value:str, is_website_owner:bool, email:str):
    cookie = db_session.query(models.Cookie).filter(models.Cookie.is_website_owner==is_website_owner).filter(models.Cookie.email==email).all()
    if len(cookie) != 1:
        return None
    cookie = cookie[0]
    cookie.cookie_value = cookie_value
    cookie.creation_time = datetime.datetime.now()

def check_cookie_exists(db_session, cookie_value):
    cookies = db_session.query(models.Cookie).filter(models.Cookie.cookie_value==cookie_value).all()
    return len(cookies) == 1

def add_cookie(db_session, cookie_value, is_website_owner, email):
    db_cookie = models.Cookie(cookie_value=cookie_value, email=email, is_website_owner=is_website_owner, creation_time=datetime.datetime.now())
    db_session.add(db_cookie)

def get_email_from_cookie_and_is_website_owner(db_session, cookie_value:str, is_website_owner:bool):
    cookie = db_session.query(models.Cookie).filter(models.Cookie.cookie_value==cookie_value).all()
    if len(cookie) != 1:
        return None
    cookie = cookie[0]
    if cookie.is_website_owner != is_website_owner:
        return None
    creation_time_difference = datetime.datetime.now() - cookie.creation_time

    if creation_time_difference.days > DAYS_COOKIE_IS_VALID:
        return None

    return cookie.email

def delete_cookie_if_it_exists(db_session, cookie_value:str):
    cookie = db_session.query(models.Cookie).filter(models.Cookie.cookie_value==cookie_value).all()
    if len(cookie) != 1:
        return
    cookie = cookie[0]
    db_session.delete(cookie)

def add_or_update_cookie_entry(db_session, cookie_value:str, is_website_owner:bool, email:str):
    if cookie_entry_exists(db_session, is_website_owner, email):
        return update_cookie_entry(db_session, cookie_value, is_website_owner, email)
    return add_cookie(db_session, cookie_value, is_website_owner, email)