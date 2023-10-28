from . import crud 
from .database import Database
from src.config import settings
from tg.util import Bunch
from src import models

from src.netarmor_api import App, Endpoint

def get_users(skip: int = 0, limit: int = 100):
    db_session = Database().get_session()
    users = crud.get_users(db_session, skip=skip, limit=limit)
    ret = []
    for i, user in enumerate(users):
        ret.append({"id" : i, "email" : user.email})
    return ret

def check_credential(email, password):
    db_session = Database().get_session()
    db_user = crud.get_user_by_email(db_session, email=email)
    if db_user is None:
        return False
    return db_user.password == password

def account_exists(email, password):
    db_session = Database().get_session()
    db_user = crud.get_user_by_email(db_session, email=email)
    return db_user is not None

def create_account(email, password):
    db_session = Database().get_session()
    db_user = crud.get_user_by_email(db_session, email=email)
    #TODO: Look into better error handling so that the react side can see this...
    if db_user:
        return False
    crud.create_user(db=db_session, email=email, password=password)
    return True

def basic_endpoint():
    return "Hello World"

def create_website_owner(email, password):
    db_session = Database().get_session()
    db_user = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email == email).first()
    if db_user:
        return False
    website_owner = models.WebsiteOwner(email=email, password=password)
    db_session.add(website_owner)
    db_session.commit()
    db_session.refresh(website_owner)
    return True

def website_owner_exists(email):
    db_session = Database().get_session()
    db_website_owner = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email == email).first()
    return db_website_owner is not None

def get_website_owners(skip: int = 0, limit: int = 100):
    db_session = Database().get_session()
    website_owners = db_session.query(models.WebsiteOwner).offset(skip).limit(limit).all()
    ret = []
    for i, website_owner in enumerate(website_owners):
        ret.append({"email" : website_owner.email, "password" :  website_owner.password})
    return ret

def get_website_owner(email):
    db_session = Database().get_session()
    db_website_owner = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email == email).first()
    ret = {"email" : db_website_owner.email, "password" :  db_website_owner.password}
    return ret

def update_website_owner_password(email, password):
    db_session = Database().get_session()
    db_website_owner = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email == email).first()
    if db_website_owner is None:
        return False
    db_website_owner.password = password
    db_session.commit()
    db_session.refresh(db_website_owner)
    return True

def delete_website_owner(email):
    db_session = Database().get_session()
    db_website_owner = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email == email).first()
    if db_website_owner is None:
        return False
    db_session.delete(db_website_owner)
    db_session.commit()
    return True

def add_website(url, email, website_name):
    db_session = Database().get_session()
    db_url = db_session.query(models.Website).filter(models.Website.url == url).first()
    if db_url:
        return False
    website = models.Website(url=url, owner=email, website_name=website_name)
    db_session.add(website)
    db_session.commit()
    db_session.refresh(website)
    return True

def website_exists(url):
    db_session = Database().get_session()
    db_website = db_session.query(models.WebsiteOwner).filter(models.Website.url == url).first()
    return db_website

def register_endpoints(app:App):
    app.register_endpoint("users", get_users, Endpoint.GET)
    app.register_endpoint("CheckCredentials", check_credential, Endpoint.GET)
    app.register_endpoint("AccountExists", account_exists, Endpoint.GET)
    app.register_endpoint("CreateAccount", create_account, Endpoint.POST)
    app.register_endpoint("basic_endpoint", basic_endpoint, Endpoint.GET)

def main():
    db = Database()
    app = App()
    register_endpoints(app)
    
    def init_model(engine):
        db.get_session().configure(bind=engine)

    model_bunch = Bunch(
        DBSession=db.get_session(),
        init_model=init_model
    )
    app.run(settings.DATABASE_API_HOST_NAME, int(settings.DATABASE_API_PORT), db.get_url(), model_bunch)

if __name__ == "__main__":
    main()