from . import crud, certificate_functions
from .database import Database
from src.config import settings

def add_cert(image, email):
    print("Adding certifcation to", email)
    db_session = Database().get_session()
    certificate_functions.add_issued_certification(db_session, image, email)
    print("Added certifcation to", email)
    db_session.commit()
    return True

    