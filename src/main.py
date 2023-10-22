from . import crud, models 
from src.config import settings
from .database import engine

from src.database import SQLALCHEMY_DATABASE_URL
from tg.util import Bunch
from sqlalchemy.orm import scoped_session, sessionmaker

from src.netarmor_api import App, Endpoint


models.Base.metadata.create_all(bind=engine)
DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))

def init_model(engine):
    DBSession.configure(bind=engine)

def get_users(skip: int = 0, limit: int = 100):
    users = crud.get_users(DBSession, skip=skip, limit=limit)
    ret = []
    for i, user in enumerate(users):
        ret.append({"id" : i, "email" : user.email})
    return ret

def check_credential(email, password):
    db_user = crud.get_user_by_email(DBSession, email=email)
    if db_user is None:
        return {"data" : False}
    return db_user.password == password


def account_exists(email, password):
    db_user = crud.get_user_by_email(DBSession, email=email)
    return db_user is not None

def create_account(email, password):
    db_user = crud.get_user_by_email(DBSession, email=email)
    #TODO: Look into better error handling so that the react side can see this...
    if db_user:
        return False
    crud.create_user(db=DBSession, email=email, password=password)
    return True

def test_endpoint():
    return "Hello World"

app = App()

app.register_endpoint("users", get_users, Endpoint.GET)
app.register_endpoint("CheckCredentials", check_credential, Endpoint.GET)
app.register_endpoint("AccountExists", account_exists, Endpoint.GET)
app.register_endpoint("CreateAccount", create_account, Endpoint.POST)
app.register_endpoint("test_endpoint", test_endpoint, Endpoint.GET)

model_bunch = Bunch(
    DBSession=DBSession,
    init_model=init_model
)
app.run(settings.DATABASE_API_HOST_NAME, int(settings.DATABASE_API_PORT), SQLALCHEMY_DATABASE_URL, model_bunch)