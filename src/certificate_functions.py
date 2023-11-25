from src import models

# Issued Certification Functions
def check_issued_certification(db_session, image, recipient):
    issued_certifications = db_session.query(models.IssuedCertification).filter(
                                                        models.IssuedCertification.image==image
                                                        and models.IssuedCertification.recipient==recipient).all()
    if len(issued_certifications) != 1:
        return False
    issued_certification = issued_certifications[0]
    return issued_certification is not None


def add_issued_certification(db_session, image, recipient):
    db_certification = models.IssuedCertification(image=image, 
                                                  recipient=recipient)
    db_session.add(db_certification)