from unittest.mock import patch
import pytest
from src.main import basic_endpoint, create_account
from src.database import Database
from src import models
from sqlalchemy.orm import Query

def test_basic():
    assert 1 == 1

def test_basic_endpoint():
    assert basic_endpoint() == "Hello World"

def test_create_user():
    create_account("micky@mouse.com", "12345")
    