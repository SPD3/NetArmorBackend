from unittest.mock import patch
import pytest
from src.main import *

def test_basic():
    assert 1 == 1

def test_basic_endpoint():
    assert basic_endpoint() == "Hello World"

def test_create_user():
    create_account("micky@mouse.com", "12345")
    assert account_exists("micky@mouse.com", "12345")

def test_create_website_owner():
    create_website_owner("micky@mouse.com", "12345")
    assert website_owner_exists("micky@mouse.com")

def test_get_website_owners():
    create_website_owner("micky@mouse.com", "12345")
    create_website_owner("minnie@mouse.com", "6789")
    assert (get_website_owners() == [{"email" : "micky@mouse.com", "password" :  "12345"},
                                    {"email" : "minnie@mouse.com", "password" :  "6789"}])

def test_get_website_owner():
    create_website_owner("micky@mouse.com", "12345")
    create_website_owner("minnie@mouse.com", "6789")
    assert (get_website_owner("micky@mouse.com") == {"email" : "micky@mouse.com", "password" :  "12345"})
    
def test_update_website_owner_password():
    create_website_owner("micky@mouse.com", "12345")
    update_website_owner_password("micky@mouse.com", "6789")
    assert (get_website_owner("micky@mouse.com")["password"] == "6789")

def test_delete_website_owner():
    create_website_owner("micky@mouse.com", "12345")
    delete_website_owner("micky@mouse.com")
    assert not website_owner_exists("micky@mouse.com")

def test_add_website():
    create_website_owner("micky@mouse.com", "12345")
    add_website("https://jiminator.github.io/Midterm/", "micky@mouse.com", "jimmy's website")
    
    db_session = Database().get_session()
    db_session.add()
    assert website_exists("https://jiminator.github.io/Midterm/")
    