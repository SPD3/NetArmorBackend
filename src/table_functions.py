from src import models
import pytest
from datetime import date
        
# Website Owner Functions
def check_website_owner(db_session, email, password, first_name, last_name):
    website_owner = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email==email).first()
    return website_owner is not None and (website_owner.password == password
                                          and website_owner.first_name == first_name
                                          and website_owner.last_name == last_name)

def check_mickey(db_session):
    return check_website_owner(db_session, "mickey@mouse.com", "12345", "Mickey", "Mouse")
    
def add_website_owner(db_session, email, password, first_name, last_name):
    db_website = models.WebsiteOwner(email=email, password=password, first_name=first_name, last_name=last_name)
    db_session.add(db_website)
    
def add_mickey(db_session):
    add_website_owner(db_session, "mickey@mouse.com", "12345", "Mickey", "Mouse")

# Website Functions
def check_website(db_session, url, owner_email, website_name):
    website = db_session.query(models.Website).filter(models.Website.url==url).first()
    return website is not None and website.owner_email == owner_email and website.website_name == website_name

def check_mickey_website(db_session):
    return check_website(db_session, "mickeymousewebsite.com", "mickey@mouse.com", "Mickey's Website")

def add_website(db_session, url, owner_email, website_name):
    db_website = models.Website(url=url, owner_email=owner_email, website_name=website_name)
    db_session.add(db_website)
    
def add_mickey_website(db_session):
    add_website(db_session, "mickeymousewebsite.com", "mickey@mouse.com", "Mickey's Website")

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

def add_resource(db_session, resource_url, title, vulnerability):
    db_resource = models.Resource(resource_url=resource_url, title=title, vulnerability=vulnerability)
    db_session.add(db_resource)
    
def add_sqli_resource(db_session):
    add_resource(db_session, "https://owasp.org/www-community/attacks/SQL_Injection", "SQL Injection", "SQL Injection")

# Cybersecurity Expert Functions
def check_cybersecurity_expert(db_session, email, password, first_name, last_name):
    cybersecurity_expert = db_session.query(models.CybersecurityExpert).filter(models.CybersecurityExpert.email==email).first()
    return cybersecurity_expert  is not None and (cybersecurity_expert.password == password 
                                                  and cybersecurity_expert.first_name == first_name
                                                  and cybersecurity_expert.last_name == last_name)

def check_donald(db_session):
    return check_cybersecurity_expert(db_session, "donald@duck.com", "12345", "Donald", "Duck")
    
def add_cybersecurity_expert(db_session, email, password, first_name, last_name):
    db_cybersecurity_expert = models.CybersecurityExpert(email=email, 
                                                         password=password, 
                                                         first_name=first_name, 
                                                         last_name=last_name)
    db_session.add(db_cybersecurity_expert)
    
def add_donald(db_session):
    add_cybersecurity_expert(db_session, "donald@duck.com", "12345", "Donald", "Duck")
    
# Specialiy Functions
def check_specialty(db_session, expert, vulnerability):
    specialty = db_session.query(models.Specialty).filter(models.Specialty.expert==expert 
                                                          and models.Specialty.vulnerability==vulnerability).first()
    return specialty is not None

def check_donald_specialty(db_session):
    return check_specialty(db_session, "donald@duck.com", "SQL Injection")
    
def add_specialty(db_session, expert, vulnerability):
    db_cybersecurity_expert = models.Specialty(expert=expert, vulnerability=vulnerability)
    db_session.add(db_cybersecurity_expert)
    
def add_donald_specialty(db_session):
    add_specialty(db_session, "donald@duck.com", "SQL Injection")


# Issued Certification Functions
def check_issued_certification(db_session, certification_number, certification_name, issuer, recipient, date_issued):
    issued_certification = db_session.query(models.IssuedCertification).filter(
                                                        models.IssuedCertification.certification_number==certification_number
                                                        and models.IssuedCertification.certification_name==certification_name
                                                        and models.IssuedCertification.issuer==issuer).first()
    return issued_certification is not None and (issued_certification.recipient == recipient 
                                                 and issued_certification.date_issued == date_issued)

def check_issued_pentest_certification(db_session):
    return check_issued_certification(db_session, 12345, "PenTest+", "CompTIA", "donald@duck.com", date.today())

def add_issued_certification(db_session, certification_number, certification_name, issuer, recipient, date_issued):
    db_certification = models.IssuedCertification(certification_number=certification_number, 
                                                  certification_name=certification_name, 
                                                  issuer=issuer, 
                                                  recipient=recipient,
                                                  date_issued=date_issued)
    db_session.add(db_certification)
    
def add_issued_pentest_certification(db_session):
    add_issued_certification(db_session, 12345, "PenTest+", "CompTIA", "donald@duck.com", date.today())

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


# FoundVulnerabilities Functions
def check_found_vulnerability(db_session, scan_id, vulnerability):
    found_vulnerability = db_session.query(models.FoundVulnerability).filter(models.FoundVulnerability.scan_id==scan_id
                                                        and models.FoundVulnerability.vulnerability==vulnerability).first()
    return found_vulnerability is not None 

def check_found_sqli(db_session):
    return check_found_vulnerability(db_session, 1, "SQL Injection")

def add_found_vulnerability(db_session, scan_id, vulnerability): 
    db_found_vulnerability = models.FoundVulnerability(vulnerability=vulnerability, scan_id=scan_id)
    db_session.add(db_found_vulnerability)
    
def add_found_sqli(db_session):
    add_found_vulnerability(db_session, 1, "SQL Injection")

# ResourceRating Functions
def check_resource_rating(db_session, website_owner, resource_url, rating):
    resource_rating = db_session.query(models.ResourceRating).filter(models.ResourceRating.website_owner==website_owner
                                                        and models.ResourceRating.resource_url==resource_url).first()
    return resource_rating is not None and (resource_rating.rating == rating)

def check_sqli_rating(db_session):
    return check_resource_rating(db_session, "mickey@mouse.com", "https://owasp.org/www-community/attacks/SQL_Injection", 5)

def add_resource_rating(db_session, email, resource_url, rating):
    db_resource_rating = models.ResourceRating(website_owner=email, resource_url=resource_url, rating=rating)
    db_session.add(db_resource_rating)
    
def add_sqli_rating(db_session):
    add_resource_rating(db_session, "mickey@mouse.com", "https://owasp.org/www-community/attacks/SQL_Injection", 5)
    
# CybersecurityExpert Rating Functions
def check_cybersecurity_expert_rating(db_session, website_owner, cybersecurity_expert, rating):
    cybersecurity_expert_rating = db_session.query(models.CybersecurityExpertRating).filter(
                                        models.CybersecurityExpertRating.website_owner==website_owner
                                        and models.CybersecurityExpertRating.cybersecurity_expert==cybersecurity_expert).first()
    return cybersecurity_expert_rating is not None and (cybersecurity_expert_rating.rating == rating)

def check_donald_rating(db_session):
    return check_cybersecurity_expert_rating(db_session, "mickey@mouse.com", "donald@duck.com", 5)

def add_cybersecurity_expert_rating(db_session, email, expert_email, rating):
    db_expert_rating = models.CybersecurityExpertRating(website_owner=email, cybersecurity_expert=expert_email, rating=rating)
    db_session.add(db_expert_rating)
    
def add_donald_rating(db_session):
    add_cybersecurity_expert_rating(db_session, "mickey@mouse.com", "donald@duck.com", 5)