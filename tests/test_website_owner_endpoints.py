from tests.constants import MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE, MINNIE_IMAGE, MINNIE_URL
from src.website_owner_endpoints import get_scan_results, add_scan_result
from src import models
from tests.helpers.website_helpers import add_mock_website
from src.database import Database

def test_add_scan_result():
    session = Database().get_session()
    add_mock_website(session, url=MINNIE_URL, email=MINNIE_EMAIL)
    session.commit()
    res = {}
    scan_results = {
        "email" : MINNIE_EMAIL,
        "res" : res,
        "url" : MINNIE_URL,
        "scan_type" : "deep_scan"
    }
    
    def get_scans():
        return session.query(models.Scan).filter(models.Scan.website_owner==scan_results["email"]).filter(models.Scan.website_url==scan_results["url"]).filter(models.Scan.deep== (scan_results["scan_type"] == "deep_scan")).all()
    assert len(get_scans()) == 0
    add_scan_result(scan_results)
    scan = get_scans()
    assert len(scan) == 1
    scan = scan[0]
    vulnerabilities = scan.tested_vulnerabilities
    assert len(vulnerabilities) == len(res.keys())
    for vulnerability in vulnerabilities:
        vulnerability_name = vulnerability.vulnerability
        assert vulnerability_name in res
        assert vulnerability.score == res[vulnerability_name]["score"]
        assert vulnerability.success == res[vulnerability_name]["success"]
        assert vulnerability.description == res[vulnerability_name]["description"]


