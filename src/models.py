from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class WebsiteOwner(Base):
    __tablename__ = 'website_owners'
    
    email = Column(String, primary_key=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    websites = relationship("Website", back_populates="owner")


class Website(Base):
    __tablename__ = 'websites'
    
    url = Column(String, primary_key=True, nullable=False, index=True)
    owner_email = Column(String, ForeignKey("website_owners.email"), nullable=False)
    website_name = Column(String, nullable=False)
    owner = relationship("WebsiteOwner", back_populates="websites")
    
class Resource(Base):
    __tablename__ = 'resources'
    
    resource_url = Column(String, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False) 
    vulnerability = Column(String, ForeignKey('vulnerabilities.name'), nullable=False)
    vulnerabilities = relationship("Vulnerability", back_populates="resources")


class Certification(Base):
    __tablename__ = 'certifications'
    
    name = Column(String, primary_key=True, nullable=False, index=True) 
    issuer = Column(String, primary_key=True, nullable=False)
    launch_date = Column(Date, nullable=False)
    certifications_issued = relationship("IssuedCertification", back_populates="certificate")


class IssuedCertification(Base):
    __tablename__ = 'issued_certifications'
    
    certification_number = Column(Integer, primary_key=True, nullable=False, index=True)
    certification_name = Column(String, primary_key=True, nullable=False)
    issuer = Column(String, primary_key=True, nullable=False)
    recipient = Column(String, ForeignKey('cybersecurity_experts.email'), nullable=False)
    date_issued = Column(Date, nullable=False)
    __table_args__ = (ForeignKeyConstraint([certification_name, issuer],
                                           [Certification.name, Certification.issuer]),
                      {})
    expert = relationship("CybersecurityExpert", back_populates="certifications")
    certificate = relationship("Certification", back_populates="certifications_issued")

class CybersecurityExpert(Base):
    __tablename__ = 'cybersecurity_experts'
    
    email = Column(String, primary_key=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    certifications = relationship("IssuedCertification", back_populates="expert")
    specialty = relationship("Specialty", back_populates="cybersecurity_expert")
    
class Vulnerability(Base):
    __tablename__ = 'vulnerabilities'
    
    name = Column(String, primary_key=True, nullable=False, index=True)
    date_added = Column(Date, nullable=False)
    resources = relationship("Resource", back_populates="vulnerabilities")
    
class Specialty(Base):
    __tablename__ = 'specialties'
    expert = Column(String, ForeignKey('cybersecurity_experts.email'), primary_key=True, nullable=False)
    vulnerability = Column(String, ForeignKey('vulnerabilities.name'), primary_key=True, nullable=False)
    cybersecurity_expert = relationship("CybersecurityExpert", back_populates="specialty")


    
    
    




