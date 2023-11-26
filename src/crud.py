from sqlalchemy.orm import Session

from . import models, schemas


def get_website_owner_by_email(db: Session, email: str):
    return db.query(models.WebsiteOwner).filter(models.WebsiteOwner.email == email).first()


def get_website_owners(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WebsiteOwner).offset(skip).limit(limit).all()
