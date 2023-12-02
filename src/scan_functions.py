from src import models

# Scan Functions
def check_scan(db_session,website_owner, website_url, deep, date):
    scans = db_session.query(models.Scan).filter(models.Scan.website_owner==website_owner).filter(models.Scan.website_url==website_url).filter(models.Scan.deep==deep).filter(models.Scan.date==date).all()
    if len(scans) != 1:
        return False
    scan = scans[0]
    return (scan.website_owner == website_owner
            and scan.website_url == website_url
            and scan.deep == deep
            and scan.date == date)

def add_scan(db_session, owner_email, url, deep, date):
    db_scan = models.Scan(website_owner=owner_email, website_url=url, deep=deep, date=date)
    db_session.add(db_scan)
    return db_scan.scan_id
