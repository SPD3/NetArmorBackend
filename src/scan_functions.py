from src import models

# Scan Functions
def check_scan(db_session, scan_id, website_owner, website_url, score, deep, date):
    scans = db_session.query(models.Scan).filter(models.Scan.scan_id==scan_id).all()
    if len(scans) != 1:
        return False
    scan = scans[0]
    return (scan.website_owner == website_owner
            and scan.website_url == website_url
            and scan.score == score
            and scan.deep == deep
            and scan.date == date)

def add_scan(db_session, scan_id, owner_email, url, score, deep, date):
    db_scan = models.Scan(scan_id=scan_id, website_owner=owner_email, website_url=url, score=score, deep=deep, date=date)
    db_session.add(db_scan)
