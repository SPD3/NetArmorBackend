from . import crud, certificate_functions
from src.models import IssuedCertification
from .database import Database
from src.config import settings
from src import crud

def add_cert(image, email):
    db_session = Database().get_session()
    certificate_functions.add_issued_certification(db_session, image, email)
    db_session.commit()
    return True

def remove_cert(email, cert_image):
    db_session = Database().get_session()
    db_user = crud.get_expert_by_email(db_session, email=email)
    if db_user is None:
        return False
    db_cert = crud.get_certifications_by_image(db_session, image=cert_image)
    db_session.delete(db_cert)
    db_session.commit()
    return True
    