from src import models
from sqlalchemy import and_


# Cybersecurity Expert Functions
def check_cybersecurity_expert(db_session, email, password, first_name, last_name, image):
    cybersecurity_experts = db_session.query(models.CybersecurityExpert).filter(models.CybersecurityExpert.email==email).all()
    if len(cybersecurity_experts) != 1:
        return False
    cybersecurity_expert = cybersecurity_experts[0]
    return (cybersecurity_expert.password == password 
            and cybersecurity_expert.first_name == first_name
            and cybersecurity_expert.last_name == last_name
            and cybersecurity_expert.image == image)

def add_cybersecurity_expert(db_session, email, password, first_name, last_name, image=""):
    db_cybersecurity_expert = models.CybersecurityExpert(email=email, 
                                                         password=password, 
                                                         first_name=first_name, 
                                                         last_name=last_name,
                                                         image=image)
    db_session.add(db_cybersecurity_expert)

    
    
# Specialty Functions
def check_specialty(db_session, expert, vulnerability):
    specialties = db_session.query(models.Specialty).filter(and_(models.Specialty.expert==expert, models.Specialty.vulnerability==vulnerability)).all()
    if len(specialties) != 1:
        return False
    specialty = specialties[0]
    return specialty is not None

    
def add_specialty(db_session, expert, vulnerability):
    db_cybersecurity_expert = models.Specialty(expert=expert, vulnerability=vulnerability)
    db_session.add(db_cybersecurity_expert)
    
def delete_specialty(db_session, expert, vulnerability):
    db_specialty = db_session.query(models.Specialty).filter(and_(models.Specialty.expert==expert, models.Specialty.vulnerability==vulnerability)).first()
    if not db_specialty:
        return False
    db_session.delete(db_specialty)
    return True