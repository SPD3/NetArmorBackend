from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class WebsiteOwner(Base):
    __tablename__ = 'website_owners'
    
    email = Column(String, primary_key=True, nullable=False, index=True)
    password = Column(String, nullable=False)

class Website(Base):
    __tablename__ = 'websites'
    
    url = Column(String, primary_key=True, nullable=False)
    owner = Column(String, ForeignKey('website_owners.email'), nullable=False)
    website_name = Column(String, nullable=False)