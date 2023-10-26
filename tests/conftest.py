
import os
from unittest.mock import MagicMock, patch

import pytest
import docker
from docker import APIClient
from docker.errors import NotFound

from src.config import get_settings


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

def set_up_empty_test_db():
    settings = get_settings()
    
    settings.POSTGRES_PASSWORD = "password"
    settings.POSTGRES_USER = "test_user"
    settings.POSTGRES_DB = "test_db"
    settings.POSTGRES_PORT = "8003"
    settings.POSTGRES_NAME = "localhost"

    client = docker.from_env()
    try:
        testdb = client.containers.get("TestDB")
        testdb.stop()
        testdb.remove()
    except NotFound:
        pass
    testdb = client.containers.run(
        "postgres:15",
        ports={5432: int(settings.POSTGRES_PORT)},
        detach=True,
        name="TestDB",
        environment=[
            "POSTGRES_PASSWORD=" + settings.POSTGRES_PASSWORD,
            "POSTGRES_USER=" + settings.POSTGRES_USER ,
            "POSTGRES_DB=" + settings.POSTGRES_DB 
                    ],
        healthcheck={
            "test" : ["CMD-SHELL", "pg_isready -U " + settings.POSTGRES_USER + " -d " + settings.POSTGRES_DB],
            "interval" : int(5 * 1e9),
            "timeout" : int(5 * 1e9),
            "retries" : int(5 * 1e9)
        }
    )

    def get_health():
        api_client = APIClient()
        inspect_results = api_client.inspect_container(testdb.name)
        return inspect_results['State']['Health']['Status']

    while testdb.status != "running" or get_health() != "healthy":
        testdb = client.containers.get("TestDB")
    return testdb

@pytest.fixture(scope="session", autouse=True)
def mock_database():
    testdb = set_up_empty_test_db()
    yield
    testdb.stop()
    testdb.remove()