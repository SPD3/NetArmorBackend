from src import models
import pytest
from datetime import date

# Generic add and duplicate tests
def generic_add_test(check_first_entry_present, add_first_entry, check_second_entry_present, add_second_entry):
    assert not check_first_entry_present()
    add_first_entry()
    assert check_first_entry_present()
    assert not check_second_entry_present()
    add_second_entry()
    assert check_second_entry_present()
    
def generic_duplicate_test(db_session, add_entry):
    add_entry()
    with pytest.raises(Exception):  
        add_entry()
        db_session.commit()
        
# Website Owner Functions
def check_website_owner(db_session, email, password):
    website_owner = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email==email).first()
    return website_owner is not None and website_owner.password == password

def check_mickey(db_session):
    return check_website_owner(db_session, "mickey@mouse.com", "12345")
    
def add_website_owner(db_session, email, password):
    db_website = models.WebsiteOwner(email=email, password=password)
    db_session.add(db_website)
    
def add_mickey(db_session):
    add_website_owner(db_session, "mickey@mouse.com", "12345")

# Website Functions

def check_website(db_session, url, owner_email, website_name):
    website = db_session.query(models.Website).filter(models.Website.url==url).first()
    return website is not None and website.owner_email == owner_email and website.website_name == website_name

def check_mickey_website(db_session):
    return check_website(db_session, "mickeymousewebsite.com", "mickey@mouse.com", "Mickey's Website")

def add_website(db_session, url, owner_email, password, website_name):
    add_website_owner(db_session, owner_email, password)
    db_website = models.Website(url=url, owner_email=owner_email, website_name=website_name)
    db_session.add(db_website)
    
def add_mickey_website(db_session):
    add_website(db_session, "mickeymousewebsite.com", "mickey@mouse.com", "12345", "Mickey's Website")

# Certification Functions

def check_certification(db_session, name, issuer, launch_date):
    certification = db_session.query(models.Certification).filter(models.Certification.name==name 
                                                                  and models.Certification.issuer==issuer).first()
    return certification is not None and certification.launch_date == launch_date

def check_pentest_certification(db_session):
    return check_certification(db_session, "PenTest+", "CompTIA", date(2020, 10, 28))

def add_certification(db_session, name, issuer, launch_date):
    db_certification = models.Certification(name=name, issuer=issuer, launch_date=launch_date)
    db_session.add(db_certification)
    
def add_pentest_certification(db_session):
    add_certification(db_session, "PenTest+", "CompTIA", date(2020, 10, 28))
    
# Vulnerability Functions

def check_vulnerability(db_session, name, date_added):
    vulnerability = db_session.query(models.Vulnerability).filter(models.Vulnerability.name==name).first()
    return vulnerability is not None and vulnerability.date_added == date_added

def check_sqli_vulnerability(db_session):
    return check_vulnerability(db_session, "SQL Injection", date.today())

def add_vulnerability(db_session, name, date_added):
    db_vulnerability = models.Vulnerability(name=name, date_added=date_added)
    db_session.add(db_vulnerability)
    
def add_sqli_vulnerability(db_session):
    add_vulnerability(db_session, "SQL Injection", date.today())
    
# Resource Functions

def check_resource(db_session, resource_url, title, vulnerability):
    resource = db_session.query(models.Resource).filter(models.Resource.resource_url==resource_url).first()
    return resource is not None and (resource.title == title and resource.vulnerability == vulnerability)

def check_sqli_resource(db_session):
    return check_resource(db_session, "https://owasp.org/www-community/attacks/SQL_Injection", "SQL Injection", "SQL Injection")

def add_resource(db_session, resource_url, title, vulnerability, date_added):
    add_vulnerability(db_session, vulnerability, date_added)
    db_resource = models.Resource(resource_url=resource_url, title=title, vulnerability=vulnerability)
    db_session.add(db_resource)
    
def add_sqli_resource(db_session):
    add_resource(db_session, "https://owasp.org/www-community/attacks/SQL_Injection", "SQL Injection", "SQL Injection", date.today())

# Cybersecurity Expert Functions

def check_cybersecurity_expert(db_session, email, password, first_name, last_name):
    cybersecurity_expert = db_session.query(models.CybersecurityExpert).filter(models.CybersecurityExpert.email==email).first()
    return cybersecurity_expert  is not None and (cybersecurity_expert.password == password 
                                                  and cybersecurity_expert.first_name == first_name
                                                  and cybersecurity_expert.last_name == last_name)

def check_donald(db_session):
    return check_cybersecurity_expert(db_session, "donald@duck.com", "12345", "Donald", "Duck")
    
def add_cybersecurity_expert(db_session, email, password, first_name, last_name):
    db_cybersecurity_expert = models.CybersecurityExpert(email=email, password=password, first_name=first_name, last_name=last_name)
    db_session.add(db_cybersecurity_expert)
    
def add_donald(db_session):
    add_cybersecurity_expert(db_session, "donald@duck.com", "12345", "Donald", "Duck")
    
# Speciality Functions

def check_specialty(db_session, expert, vulnerability):
    specialty = db_session.query(models.Specialty).filter(models.Specialty.expert==expert and 
                                                                     models.Specialty.vulnerability==vulnerability).first()
    return specialty  is not None

def check_donald_specialty(db_session):
    return check_specialty(db_session, "donald@duck.com", "SQL Injection")
    
def add_specialty(db_session, expert, password, first_name, last_name, vulnerability, date_added):
    add_cybersecurity_expert(db_session, expert, password, first_name, last_name)
    add_vulnerability(db_session, vulnerability, date_added)
    db_cybersecurity_expert = models.Specialty(expert=expert, vulnerability=vulnerability)
    db_session.add(db_cybersecurity_expert)
    
def add_donald_specialty(db_session):
    add_specialty(db_session, "donald@duck.com", "12345", "Donald", "Duck", "SQL Injection", date.today())


# Issued Certification Functions

def check_issued_certification(db_session, certification_number, certification_name, issuer, recipient, date_issued):
    issued_certification = db_session.query(models.IssuedCertification).filter(models.IssuedCertification.certification_number==certification_number
                                                                  and models.IssuedCertification.certification_name==certification_name
                                                                  and models.IssuedCertification.issuer==issuer).first()
    return issued_certification is not None and (issued_certification.recipient == recipient 
                                                 and issued_certification.date_issued == date_issued)

def check_issued_pentest_certification(db_session):
    return check_issued_certification(db_session, 12345, "PenTest+", "CompTIA", "donald@duck.com", date.today())

def add_issued_certification(db_session, certification_number, certification_name, issuer, date_launched,
                             recipient, password, first_name, last_name, 
                             date_issued):
    add_certification(db_session, certification_name, issuer, date_launched)
    add_cybersecurity_expert(db_session, recipient, password, first_name, last_name)  
    db_certification = models.IssuedCertification(certification_number=certification_number, 
                                                  certification_name=certification_name, 
                                                  issuer=issuer, 
                                                  recipient=recipient,
                                                  date_issued=date_issued)
    db_session.add(db_certification)
    
def add_issued_pentest_certification(db_session):
    add_issued_certification(db_session, 12345,  "PenTest+", "CompTIA", date(2020, 10, 28),
                            "donald@duck.com", "12345", "Donald", "Duck",
                             date.today())
