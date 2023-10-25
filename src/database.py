from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from src.config import settings
from . import models
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

class Database():
    def __init__(self) -> None:
        self.url = "postgresql+psycopg2://" + settings.POSTGRES_USER + ":" + settings.POSTGRES_PASSWORD+ "@"+ settings.POSTGRES_NAME + ":"+ settings.POSTGRES_PORT+ "/" + settings.POSTGRES_DB
        self.engine = create_engine(
            self.url
        )
        models.Base.metadata.create_all(bind=self.engine)
        self.session = scoped_session(sessionmaker(autoflush=True, autocommit=False))

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance
    
    def get_url(self):
        return self.url
    
    def get_engine(self):
        return self.engine
    
    def get_session(self):
        return self.session
