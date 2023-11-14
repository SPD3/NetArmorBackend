from src.scan_functions import check_scan, add_scan
from datetime import date
from tests.constants import MICKEY_EMAIL, MICKEY_URL

def check_mickey_scan(db_session):
    return check_scan(db_session, 1, MICKEY_EMAIL, MICKEY_URL, False, date.today())

def add_mickey_scan(db_session):
    add_scan(db_session, 1, MICKEY_EMAIL, MICKEY_URL, False, date.today())