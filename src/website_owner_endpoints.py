from src import models
from src.scan_functions import add_scan
from src.vulnerability_functions import add_tested_vulnerability
from src.website_functions import add_website
from typing import Dict
import datetime
from .database import Database

SUCCESS_KEY = "success"
SCORE_KEY = "score"
DESCRIPTION_KEY = "description"

def add_scan_result(scan_results:Dict[str,object]):
    account_email = scan_results["email"]
    result = scan_results["res"]
    url = scan_results["url"]
    is_deep_scan = scan_results["scan_type"] == "deep_scan"
    scan_time = datetime.datetime.now()
    db_session = Database().get_session()
    if len(db_session.query(models.Website).filter(models.Website.url == url).all()) == 0:
        add_website(db_session=db_session, url=url, owner_email=account_email, website_name=url)
    scan_id = add_scan(db_session=db_session, owner_email=account_email, url=url, deep=is_deep_scan, date=scan_time)
    for vulnerability in result:
        add_tested_vulnerability(db_session, scan_id, vulnerability, result[vulnerability][SCORE_KEY], result[vulnerability][SUCCESS_KEY], result[vulnerability][DESCRIPTION_KEY])

    db_session.commit()

def get_scan_results(email:str):
    db_session = Database().get_session()
    scans = db_session.query(models.Scan).filter(models.Scan.website_owner==email).all()
    return_res = []
    for scan in scans:
        return_res.append({})
        res = {}
        vulnerabilities = scan.tested_vulnerabilities
        for vulnerability in vulnerabilities:
            res[vulnerability.vulnerability] = {
                SCORE_KEY : vulnerability.score,
                SUCCESS_KEY : vulnerability.success,
                DESCRIPTION_KEY : vulnerability.description
            }
        return_res[-1]["res"] = res
        return_res[-1]["url"] = scan.website_url
        return_res[-1]["date"] = scan.date
        return_res[-1]["scan_type"] = "deep_scan" if scan.deep else "basic_scan"

    return return_res
    
