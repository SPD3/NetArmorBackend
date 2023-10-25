from . import crud 
from .database import Database
from src.config import settings
from tg.util import Bunch

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
        return {"data" : False}
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