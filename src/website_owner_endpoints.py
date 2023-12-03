from src import models
from src.scan_functions import add_scan
from src.vulnerability_functions import add_tested_vulnerability
from src.website_functions import add_website
from typing import Dict, Union
import datetime
from .database import Database
from src.message_functions import add_message

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

FIRST_NAME_KEY = "first_name"
LAST_NAME_KEY = "last_name"
IMAGE_KEY = "image"
    
def create_expert_request(website_owner_email:str, cybersecurity_expert_email:str, message:str):
    db_session = Database().get_session()
    messages = db_session.query(models.Message).filter(
                                        models.Message.website_owner==website_owner_email
                                        and models.Message.cybersecurity_expert==cybersecurity_expert_email).all()
    if len(messages) != 0:
        return False
    add_message(db_session, website_owner_email, cybersecurity_expert_email, message, is_pending=True, time_sent=datetime.datetime.now())
    db_session.commit()
    return True

def get_website_owner_info(email:str):
    db_session = Database().get_session()
    website_owner = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email==email).all()
    if len(website_owner) != 1:
        return None
    website_owner = website_owner[0]

    return {
        FIRST_NAME_KEY : website_owner.first_name,
        LAST_NAME_KEY : website_owner.last_name,
        IMAGE_KEY : website_owner.image,
    }

def update_website_owner_info(email:str, image:Union[str,None], password:Union[str,None]):
    db_session = Database().get_session()
    website_owner = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email==email).all()
    if len(website_owner) != 1:
        return None
    website_owner = website_owner[0]
    if image:
        website_owner.image = image
    if password:
        website_owner.password = password
    db_session.commit()
    return 