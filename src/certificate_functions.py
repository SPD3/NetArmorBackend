from src import models
from datetime import date


# Certification Functions
def check_certification(db_session, name, issuer, launch_date):
    certifications = db_session.query(models.Certification).filter(models.Certification.name==name 
                                                                  and models.Certification.issuer==issuer).all()
    if len(certifications) != 1:
        return False
    certification = certifications[0]
    return certification.launch_date == launch_date

def add_certification(db_session, name, issuer, launch_date):
    db_certification = models.Certification(name=name, issuer=issuer, launch_date=launch_date)
    db_session.add(db_certification)
    

# Issued Certification Functions
def check_issued_certification(db_session, certification_number, certification_name, issuer, recipient, date_issued):
    issued_certifications = db_session.query(models.IssuedCertification).filter(
                                                        models.IssuedCertification.certification_number==certification_number
                                                        and models.IssuedCertification.certification_name==certification_name
                                                        and models.IssuedCertification.issuer==issuer).all()
    if len(issued_certifications) != 1:
        return False
    issued_certification = issued_certifications[0]
    return issued_certification is not None and (issued_certification.recipient == recipient 
                                                 and issued_certification.date_issued == date_issued)


def add_issued_certification(db_session, certification_number, certification_name, issuer, recipient, date_issued):
    db_certification = models.IssuedCertification(certification_number=certification_number, 
                                                  certification_name=certification_name, 
                                                  issuer=issuer, 
                                                  recipient=recipient,
                                                  date_issued=date_issued)
    db_session.add(db_certification)