from src import models
from datetime import date

# Scan Functions
def check_scan(db_session, scan_id, website_owner, website_url, deep, date):
    scan = db_session.query(models.Scan).filter(models.Scan.scan_id==scan_id).first()
    return scan is not None and (scan.website_owner == website_owner
                                and scan.website_url == website_url
                                and scan.deep == deep
                                and scan.date == date)

def check_mickey_scan(db_session):
    return check_scan(db_session, 1, "mickey@mouse.com", "mickeymousewebsite.com", False, date.today())

def add_scan(db_session, scan_id, owner_email, url, deep, date):
    db_scan = models.Scan(scan_id=scan_id, website_owner=owner_email, website_url=url, deep=deep, date=date)
    db_session.add(db_scan)
    
def add_mickey_scan(db_session):
    add_scan(db_session, 1, "mickey@mouse.com", "mickeymousewebsite.com", False, date.today())