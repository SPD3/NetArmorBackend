import datetime
from unittest import mock
from tests.constants import MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE, MINNIE_IMAGE, MINNIE_URL
from tests.constants import MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, MICKEY_IMAGE, MICKEY_EMAIL, DONALD_EMAIL, DONALD_FIRST_NAME, DONALD_IMAGE, DONALD_LAST_NAME, DONALD_PASSWORD, PENTEST_IMAGE, CLOUD_IMAGE, DAISY_EMAIL, DAISY_FIRST_NAME, DAISY_IMAGE, DAISY_LAST_NAME, DAISY_PASSWORD
from src.website_owner_endpoints import get_scan_results, add_scan_result, SUCCESS_KEY, SCORE_KEY, DESCRIPTION_KEY, create_expert_request, get_website_owner_info, FIRST_NAME_KEY, LAST_NAME_KEY, IMAGE_KEY, update_website_owner_info, get_experts, EXPERT_EMAIL_KEY, EXPERT_IMAGE_KEY, EXPERT_SPECIALTIES_KEY, EXPERT_CERTIFICATIONS_KEY, EXPERT_LAST_NAME_KEY, EXPERT_FIRST_NAME_KEY, get_experts_by_result
from src import models
from tests.helpers.website_helpers import add_mock_website
from src.website_functions import add_website_owner
from src import populate_tables
from src.database import Database
from src.website_functions import add_website_owner
from src.expert_functions import add_cybersecurity_expert
from src.expert_endpoints import create_expert_account, add_expert_info
from src.certificate_endpoints import add_cert

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
    new_scan_results = scan_results.copy()
    new_scan_results["url"] += "a"
    add_scan_result(new_scan_results)

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

def test_get_website_owner_info():
    session = Database().get_session()
    add_website_owner(session, MINNIE_EMAIL, MINNIE_PASSWORD, MINNIE_FIRST_NAME, MINNIE_LAST_NAME, MINNIE_IMAGE)
    session.commit()
    info = get_website_owner_info(MINNIE_EMAIL)
    assert info[FIRST_NAME_KEY] == MINNIE_FIRST_NAME
    assert info[LAST_NAME_KEY] == MINNIE_LAST_NAME
    assert info[IMAGE_KEY] == MINNIE_IMAGE

@mock.patch('src.website_owner_endpoints.datetime', side_effect=lambda *args, **kw: datetime.date(*args, **kw))
def test_create_expert_request(mock_date):
    mock_now = datetime.datetime(year=2023, month=1, day=10)
    mock_date.datetime.now.return_value = mock_now
    session = Database().get_session()
    add_website_owner(session, MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, image=MICKEY_IMAGE)
    add_cybersecurity_expert(session, DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME, DONALD_IMAGE)
    session.commit()
    message_str = "My Message"
    assert create_expert_request(MICKEY_EMAIL, DONALD_EMAIL, message=message_str)
    def check_message():
        messages = session.query(models.Message).filter(
                                        models.Message.website_owner==MICKEY_EMAIL
                                        and models.Message.cybersecurity_expert==DONALD_EMAIL).all()
        assert len(messages) == 1
        message = messages[0]
        assert message.is_pending
        assert message.payload == message_str
        assert message.time_sent == mock_now
        
    check_message()
    message2 = "My Message 2"
    mock_now2 = datetime.date(year=2023, month=1, day=10)
    mock_date.datetime.now.return_value = mock_now2
    assert not create_expert_request(MICKEY_EMAIL, DONALD_EMAIL, message=message2)
    check_message()

def test_update_website_owner_info():
    session = Database().get_session()
    add_website_owner(session, MICKEY_EMAIL, MICKEY_PASSWORD, MICKEY_FIRST_NAME, MICKEY_LAST_NAME, image=MICKEY_IMAGE)
    session.commit()
    def check_website_owner(password, image):
        website_owner = session.query(models.WebsiteOwner).filter(
                                        models.WebsiteOwner.email==MICKEY_EMAIL).all()
        assert len(website_owner) == 1
        website_owner = website_owner[0]
        assert website_owner.password == password
        assert website_owner.image == image
    check_website_owner(MICKEY_PASSWORD, MICKEY_IMAGE)

    update_website_owner_info(MICKEY_EMAIL, image=None, password=MICKEY_PASSWORD + "a")
    check_website_owner(MICKEY_PASSWORD + "a", MICKEY_IMAGE)
    update_website_owner_info(MICKEY_EMAIL, image=MICKEY_IMAGE + "a", password=None)
    check_website_owner(MICKEY_PASSWORD + "a", MICKEY_IMAGE + "a")
    update_website_owner_info(MICKEY_EMAIL, image=MICKEY_IMAGE, password=MICKEY_PASSWORD)
    check_website_owner(MICKEY_PASSWORD, MICKEY_IMAGE)

def test_get_experts():
    populate_tables.populate_vulnerabilities()
    create_expert_account(DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME)
    add_expert_info(DONALD_EMAIL, DONALD_IMAGE, "true", "true", "false", "false")
    add_cert(PENTEST_IMAGE, DONALD_EMAIL)
    add_cert(CLOUD_IMAGE, DONALD_EMAIL)

    create_expert_account(DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME)
    add_expert_info(DAISY_EMAIL, DAISY_IMAGE, "true", "false", "true", "true")
    add_cert(CLOUD_IMAGE, DAISY_EMAIL)
    experts = get_experts()
    assert len(experts) == 2
    expert_email_to_index = {}
    for i, expert in enumerate(experts):
        expert_email_to_index[expert[EXPERT_EMAIL_KEY]] = i
    assert DAISY_EMAIL in expert_email_to_index
    assert DONALD_EMAIL in expert_email_to_index

    daisy_res = experts[expert_email_to_index[DAISY_EMAIL]]
    assert daisy_res[EXPERT_FIRST_NAME_KEY] == DAISY_FIRST_NAME
    assert daisy_res[EXPERT_LAST_NAME_KEY] == DAISY_LAST_NAME
    assert daisy_res[EXPERT_IMAGE_KEY] == DAISY_IMAGE
    assert set(daisy_res[EXPERT_CERTIFICATIONS_KEY]) == set([CLOUD_IMAGE])
    assert set(daisy_res[EXPERT_SPECIALTIES_KEY]) == set([populate_tables.SQL_INJECTION_NAME, populate_tables.NMAP_NAME, populate_tables.JWT_COOKIE_HIJACKING_NAME])

    donald_res = experts[expert_email_to_index[DONALD_EMAIL]]
    assert donald_res[EXPERT_FIRST_NAME_KEY] == DONALD_FIRST_NAME
    assert donald_res[EXPERT_LAST_NAME_KEY] == DONALD_LAST_NAME
    assert donald_res[EXPERT_IMAGE_KEY] == DONALD_IMAGE
    assert set(donald_res[EXPERT_CERTIFICATIONS_KEY]) == set([PENTEST_IMAGE, CLOUD_IMAGE])
    assert set(donald_res[EXPERT_SPECIALTIES_KEY]) == set([populate_tables.XSS_NAME, populate_tables.SQL_INJECTION_NAME])

def test_get_experts_by_result():
    populate_tables.populate_vulnerabilities()
    create_expert_account(DONALD_EMAIL, DONALD_PASSWORD, DONALD_FIRST_NAME, DONALD_LAST_NAME)
    add_expert_info(DONALD_EMAIL, DONALD_IMAGE, "true", "true", "false", "false")
    add_cert(PENTEST_IMAGE, DONALD_EMAIL)
    add_cert(CLOUD_IMAGE, DONALD_EMAIL)

    create_expert_account(DAISY_EMAIL, DAISY_PASSWORD, DAISY_FIRST_NAME, DAISY_LAST_NAME)
    add_expert_info(DAISY_EMAIL, DAISY_IMAGE, "true", "false", "true", "true")
    add_cert(CLOUD_IMAGE, DAISY_EMAIL)
    experts = get_experts_by_result([populate_tables.SQL_INJECTION_NAME, populate_tables.NMAP_NAME])
    assert len(experts) == 1
    daisy_res = experts[0]
    assert daisy_res[EXPERT_FIRST_NAME_KEY] == DAISY_FIRST_NAME
    assert daisy_res[EXPERT_LAST_NAME_KEY] == DAISY_LAST_NAME
    assert daisy_res[EXPERT_IMAGE_KEY] == DAISY_IMAGE
    assert set(daisy_res[EXPERT_CERTIFICATIONS_KEY]) == set([CLOUD_IMAGE])
    assert set(daisy_res[EXPERT_SPECIALTIES_KEY]) == set([populate_tables.SQL_INJECTION_NAME, populate_tables.NMAP_NAME, populate_tables.JWT_COOKIE_HIJACKING_NAME])
