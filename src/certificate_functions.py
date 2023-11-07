from src import models
from datetime import date


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