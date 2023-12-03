from sqlalchemy.orm import Session

from . import models, schemas


def get_website_owner_by_email(db: Session, email: str):
    return db.query(models.WebsiteOwner).filter(models.WebsiteOwner.email == email).first()

def get_website_owners(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WebsiteOwner).offset(skip).limit(limit).all()

def get_expert_by_email(db: Session, email: str):
    return db.query(models.CybersecurityExpert).filter(models.CybersecurityExpert.email == email).first()

def get_certifications(db: Session):
    return db.query(models.IssuedCertification).all()

def get_certifications_by_image(db: Session, image: str):
    return db.query(models.IssuedCertification).filter(models.IssuedCertification.image == image).first()
    
def get_message_by_emails(db: Session, expert, owner):
    return db.query(models.Message).filter(models.Message.website_owner == owner
                                           and models.Message.cybersecurity_expert == expert).first()
