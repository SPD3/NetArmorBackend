import datetime
from unittest import mock
import pytest
from tests.constants import MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_URL, MINNIE_WEBSITE_NAME, MINNIE_IMAGE, MICKEY_EMAIL, MICKEY_URL, MICKEY_WEBSITE_NAME, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE, MINNIE_IMAGE, MICKEY_COOKIE, MINNIE_COOKIE
from src.main import create_website_owner
from src.cookies_endpoints import create_cookie, validate_cookie, delete_cookie
from src.database import Database
from src import models

@mock.patch('src.website_functions.datetime', side_effect=lambda *args, **kw: datetime.date(*args, **kw))
def test_create_cookie(mock_date):
    mock_now = datetime.datetime(year=2023, month=1, day=10, hour=10, minute=0, second=0)
    mock_date.datetime.now.return_value = mock_now
    create_website_owner(MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE)
    cookie = create_cookie(MINNIE_EMAIL, True)
    session = Database().get_session()
    def check_cookie(cookie, is_website_owner):
        cookie_entry = session.query(models.Cookie).filter(models.Cookie.cookie_value==cookie).all()
        assert len(cookie_entry) == 1
        cookie_entry = cookie_entry[0]
        assert cookie_entry.cookie_value == cookie
        assert cookie_entry.email == MINNIE_EMAIL
        assert cookie_entry.is_website_owner == is_website_owner
        assert cookie_entry.creation_time == mock_now
    
    check_cookie(cookie, True)
    cookie = create_cookie(MINNIE_EMAIL, False)
    check_cookie(cookie, False)
    cookie = create_cookie(MINNIE_EMAIL, True)
    check_cookie(cookie, True)

@mock.patch('src.website_functions.datetime', side_effect=lambda *args, **kw: datetime.date(*args, **kw))
def test_validate_cookie(mock_date):
    mock_now = datetime.datetime(year=2023, month=1, day=10, hour=10, minute=0, second=0)
    mock_date.datetime.now.return_value = mock_now
    create_website_owner(MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE)
    cookie = create_cookie(MINNIE_EMAIL, True)

    assert validate_cookie(cookie, True) == MINNIE_EMAIL
    assert validate_cookie(cookie, False) is None
    assert validate_cookie(cookie + "a", True) is None

    invalid_now = mock_now + datetime.timedelta(days=10)
    mock_date.datetime.now.return_value = invalid_now
    assert validate_cookie(cookie, True) is None 

def test_delete_cookie():
    create_website_owner(MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE)
    cookie = create_cookie(MINNIE_EMAIL, True)
    delete_cookie(cookie + "a")
    delete_cookie(cookie)
    session = Database().get_session()
    assert len(session.query(models.Cookie).filter(models.Cookie.cookie_value==cookie).all()) == 0
