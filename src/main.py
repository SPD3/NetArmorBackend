from http.client import HTTPException
from typing import List

from sqlalchemy.orm import Session

from . import crud, models, schemas 
from src.config import settings
from .database import SessionLocal, engine


import tg
from tg import decode_params, expose, AppConfig
from tg.controllers import RestController, TGController
from tg.decorators import with_trailing_slash

from src.database import SQLALCHEMY_DATABASE_URL
from wsgiref.simple_server import make_server
from tg.util import Bunch
from sqlalchemy.orm import scoped_session, sessionmaker


models.Base.metadata.create_all(bind=engine)
DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))

def init_model(engine):
    DBSession.configure(bind=engine)

class CreateAccountController(RestController):
    def _before(self, *args, **kw):
        tg.response.headers.update({'Access-Control-Allow-Origin': '*',
                                    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                                    'Access-Control-Allow-Methods' : 'GET, POST, PUT'})

    @with_trailing_slash
    @expose()
    def get(self):
        return {"data" : "Hello World"}

    @expose()
    @decode_params('json')
    def post(self, *args, **kw):
        email = kw["email"]
        password = kw["password"]
        db_user = crud.get_user_by_email(DBSession, email=email)
        #TODO: Look into better error handling so that the react side can see this...
        if db_user:
            return {"err": "Email already registered"}
        crud.create_user(db=DBSession, email=email, password=password)
        return {"data": True, "args" : args, "kw" : kw}
    
class AccountExistsController(RestController):
    def _before(self, *args, **kw):
        tg.response.headers.update({'Access-Control-Allow-Origin': '*'})

    @with_trailing_slash
    @expose()
    def get(self, email):
        db_user = crud.get_user_by_email(DBSession, email=email)
        return {"data" : db_user is not None}
    
class CheckCredentialsController(RestController):
    def _before(self, *args, **kw):
        tg.response.headers.update({'Access-Control-Allow-Origin': '*'})
        

    @with_trailing_slash
    @expose()
    def get(self, email, password):
        db_user = crud.get_user_by_email(DBSession, email=email)
        if db_user is None:
            return {"data" : False}
        return {"data" : db_user.password == password}
    
class UsersController(RestController):
    def _before(self, *args, **kw):
        tg.response.headers.update({'Access-Control-Allow-Origin': '*'})

    @with_trailing_slash
    @expose()
    def get(self, skip: int = 0, limit: int = 100):
        users = crud.get_users(DBSession, skip=skip, limit=limit)
        ret = []
        for i, user in enumerate(users):
            ret.append({"id" : i, "email" : user.email})
        return {"data" : ret}

class RootController(TGController):
    def _before(self, *args, **kw):
        tg.response.headers.update({'Access-Control-Allow-Origin': '*',
                                    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                                    'Access-Control-Allow-Methods' : 'GET, POST, PUT'})

    CreateAccount = CreateAccountController()
    AccountExists = AccountExistsController()
    CheckCredentials = CheckCredentialsController()
    users = UsersController()
    
config = AppConfig(minimal=True, root_controller=RootController())
config['use_sqlalchemy'] = True
config['sqlalchemy.url'] = SQLALCHEMY_DATABASE_URL
config['model'] = Bunch(
    DBSession=DBSession,
    init_model=init_model
)
config.sa_auth.authmetadata = None

application = config.make_wsgi_app()

httpd = make_server(settings.DATABASE_API_HOST_NAME, int(settings.DATABASE_API_PORT), application)
httpd.serve_forever()

