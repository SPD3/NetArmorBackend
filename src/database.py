from sqlalchemy import create_engine
from src.config import settings
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base

class Database():
    def __init__(self) -> None:
        self.url = "postgresql+psycopg2://" + settings.POSTGRES_USER + ":" + settings.POSTGRES_PASSWORD+ "@"+ settings.POSTGRES_NAME + ":"+ settings.POSTGRES_PORT+ "/" + settings.POSTGRES_DB
        self.engine = create_engine(
            self.url
        )
        Base.metadata.create_all(bind=self.engine)
        self._session = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=self.engine))

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance
    
    def get_url(self):
        return self.url
    
    def get_engine(self):
        return self.engine
    
    def get_session(self):
        self._session.rollback()
        return self._session
