from . import crud, website_functions
from .database import Database
from src.config import settings
from tg.util import Bunch

from src.netarmor_api import App, Endpoint
from src.cookies_endpoints import create_cookie, validate_cookie, delete_cookie
from src.expert_endpoints import check_expert_info, expert_exists, create_expert_account, delete_expert, add_expert_info
from src.website_owner_endpoints import add_scan_result, get_scan_results, create_expert_request
from src.populate_tables import populate_tables
from datetime import date
from sqlalchemy import event
from src.models import Base
import contextlib

from src import models


def check_website_owner_credentials(email, password):
    db_session = Database().get_session()
    db_user = crud.get_website_owner_by_email(db_session, email=email)
    if db_user is None:
        return False
    return db_user.password == password

def website_owner_exists(email):
    db_session = Database().get_session()
    db_user = crud.get_website_owner_by_email(db_session, email=email)
    return db_user is not None

def create_website_owner(email, password, first_name, last_name, image):
    db_session = Database().get_session()
    db_user = crud.get_website_owner_by_email(db_session, email)
    #TODO: Look into better error handling so that the react side can see this...
    if db_user:
        return False
    website_functions.add_website_owner(db_session, email, password, first_name, last_name, image)
    db_session.commit()
    return True

def delete_website_owner(email):
    db_session = Database().get_session()
    db_user = crud.get_website_owner_by_email(db_session, email)
    if not db_user:
        return False
    db_session.delete(db_user)
    db_session.commit()
    return True

def delete_all_table_contents():
    meta = Base.metadata
    with contextlib.closing(Database().get_engine().connect()) as con:
        trans = con.begin()
        tables = meta.sorted_tables
        for table in reversed(tables):
            con.execute(table.delete())
        trans.commit()

def clear_tables():
    delete_all_table_contents()

def register_endpoints(app:App):
    app.register_endpoint("check_website_owner_credentials", check_website_owner_credentials, Endpoint.GET)
    app.register_endpoint("website_owner_exists", website_owner_exists, Endpoint.GET)
    app.register_endpoint("create_website_owner", create_website_owner, Endpoint.POST)
    app.register_endpoint("delete_website_owner", delete_website_owner, Endpoint.POST)
    app.register_endpoint("check_expert_info", check_expert_info, Endpoint.GET)
    app.register_endpoint("expert_exists", expert_exists, Endpoint.GET)
    app.register_endpoint("create_expert_account", create_expert_account, Endpoint.POST)
    app.register_endpoint("delete_expert", delete_expert, Endpoint.POST)
    app.register_endpoint("add_expert_info", add_expert_info, Endpoint.POST)


    app.register_endpoint("create_cookie", create_cookie, Endpoint.POST)
    app.register_endpoint("validate_cookie", validate_cookie, Endpoint.GET)
    app.register_endpoint("delete_cookie", delete_cookie, Endpoint.POST)

    app.register_endpoint("get_scan_results", get_scan_results, Endpoint.GET)
    app.register_endpoint("add_scan_result", add_scan_result, Endpoint.POST)
    app.register_endpoint("create_expert_request", create_expert_request, Endpoint.POST)

    app.register_endpoint("clear_tables", clear_tables, Endpoint.GET)

def main():
    db = Database()
    app = App()
    register_endpoints(app)
    
    def init_model(engine):
        db.get_session(False).configure(bind=engine)

    model_bunch = Bunch(
        DBSession=db.get_session(False),
        init_model=init_model
    )
     
    app.run(settings.DATABASE_API_HOST_NAME, int(settings.DATABASE_API_PORT), db.get_url(), model_bunch, run_before_hosting=populate_tables)

if __name__ == "__main__":
    main()