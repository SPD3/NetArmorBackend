import datetime
from unittest import mock
from tests.constants import MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE, MINNIE_IMAGE, MINNIE_URL
from src.website_owner_endpoints import get_scan_results, add_scan_result, SUCCESS_KEY, SCORE_KEY, DESCRIPTION_KEY
from src import models
from tests.helpers.website_helpers import add_mock_website
from src import populate_tables
from src.database import Database

res = {
    populate_tables.NMAP_NAME : {
        SUCCESS_KEY : True,
        SCORE_KEY : 100,
        DESCRIPTION_KEY : ""
    },
    populate_tables.JWT_COOKIE_HIJACKING_NAME : {
        SUCCESS_KEY : False,
        SCORE_KEY : 0,
        DESCRIPTION_KEY : ""
    },
    populate_tables.XSS_NAME : {
        SUCCESS_KEY : True,
        SCORE_KEY : 0,
        DESCRIPTION_KEY : "XSS"
    },
    populate_tables.SQL_INJECTION_NAME : {
        SUCCESS_KEY : True,
        SCORE_KEY : 20,
        DESCRIPTION_KEY : "Some SQL injection problems"
    },
}
scan_results = {
    "email" : MINNIE_EMAIL,
    "res" : res,
    "url" : MINNIE_URL,
    "scan_type" : "deep_scan"
}

@mock.patch('src.website_owner_endpoints.datetime', side_effect=lambda *args, **kw: datetime.date(*args, **kw))
def test_add_scan_result(mock_date):
    mock_now = datetime.date(year=2023, month=1, day=10)
    mock_date.datetime.now.return_value = mock_now
    populate_tables.populate_vulnerabilities()
    session = Database().get_session()
    add_mock_website(session, url=MINNIE_URL, email=MINNIE_EMAIL)
    session.commit()
    
    def get_scans():
        return session.query(models.Scan).filter(models.Scan.website_owner==scan_results["email"]).filter(models.Scan.website_url==scan_results["url"]).filter(models.Scan.deep== (scan_results["scan_type"] == "deep_scan")).all()
    assert len(get_scans()) == 0
    add_scan_result(scan_results)
    scan = get_scans()
    assert len(scan) == 1
    scan = scan[0]
    assert scan.date == mock_now
    vulnerabilities = scan.tested_vulnerabilities
    assert len(vulnerabilities) == len(res.keys())
    for vulnerability in vulnerabilities:
        vulnerability_name = vulnerability.vulnerability
        assert vulnerability_name in res
        assert vulnerability.score == res[vulnerability_name]["score"]
        assert vulnerability.success == res[vulnerability_name]["success"]
        assert vulnerability.description == res[vulnerability_name]["description"]

@mock.patch('src.website_owner_endpoints.datetime', side_effect=lambda *args, **kw: datetime.date(*args, **kw))
def test_get_scan_results(mock_date):
    mock_now = datetime.date(year=2023, month=1, day=10)
    mock_date.datetime.now.return_value = mock_now
    populate_tables.populate_vulnerabilities()
    session = Database().get_session()
    add_mock_website(session, url=MINNIE_URL, email=MINNIE_EMAIL)
    session.commit()
    scan_results_num = 5
    for i in range(scan_results_num):
        add_scan_result(scan_results)
    
    minnies_scans = get_scan_results(MINNIE_EMAIL)
    assert len(minnies_scans) == scan_results_num
    for scan in minnies_scans:
        assert scan["res"] == res
        assert scan["url"] == scan_results["url"]
        assert scan["scan_type"] == scan_results["scan_type"]
        assert scan["date"] == mock_now

