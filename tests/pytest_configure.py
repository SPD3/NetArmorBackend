
from unittest.mock import MagicMock, patch

import pytest
from src.database import Database

class Fake_Database:
    def get_url(self):
        return "fake_url"
    
    def get_engine(self):
        return None
    
    def get_session(self):
        return Fake_Session()

class Fake_Session:
    def query(*args):
        print("querying!")
        return []

    def add(*args):
        print("adding!")

    def commit(*args):
        print("committing!")

    def refresh(*args):
        print("refreshing!")

# def pytest_sessionstart(session):
#     """
#     Called after the Session object has been created and
#     before performing collection and entering the run test loop.
#     """
#     # Database.__new__ = MagicMock(return_value=Fake_Database())
#     def mock_constructor(self):
#         self.url = ""
#         self.engine = None
#         self.session = Fake_Session()
#     with patch.object(Database, "__init__", mock_constructor):
#         yield

@pytest.fixture(scope="session", autouse=True)
def mock_database():
    def mock_constructor(self):
        self.url = ""
        self.engine = None
        self.session = Fake_Session()
    with patch.object(Database, "__init__", mock_constructor):
        yield

    

# def pytest_sessionfinish(session, exitstatus):
#     """
#     Called after whole test run finished, right before
#     returning the exit status to the system.
#     """