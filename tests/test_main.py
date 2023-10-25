from unittest.mock import patch
import pytest
from src.main import basic_endpoint, create_account
from src.database import Database
from src import models
from sqlalchemy.orm import Query

class Fake_Query:

    def filter(*args, **kwargs):
        return Fake_Query()
    
    def first(*args, **kwargs):
        return None

class Fake_Session:
    def query(*args, **kwargs):
        print("querying!")
        return Fake_Query()

    def add(*args, **kwargs):
        print("adding!")

    def commit(*args, **kwargs):
        print("committing!")

    def refresh(*args, **kwargs):
        print("refreshing!")

@pytest.fixture(scope="session", autouse=True)
def mock_database():
    def mock_constructor(self):
        self.url = ""
        self.engine = None
        self.session = Fake_Session()
    with patch.object(Database, "__init__", mock_constructor):
        yield

def test_basic():
    assert 1 == 1

def test_basic_endpoint():
    assert basic_endpoint() == "Hello World"

def test_create_user():
    create_account("micky@mouse.com", "12345")