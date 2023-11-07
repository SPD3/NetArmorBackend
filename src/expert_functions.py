from src import models

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
    
    
# Specialty Functions
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