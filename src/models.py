from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, ForeignKeyConstraint, CheckConstraint
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
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    websites = relationship("Website", back_populates="owner")
    scans = relationship("Scan", back_populates="owner")
    resource_ratings = relationship("ResourceRating", back_populates="owner")
    cybersecurity_expert_ratings = relationship("CybersecurityExpertRating", back_populates="owner")
    
class Website(Base):
    __tablename__ = 'websites'
    
    url = Column(String, primary_key=True, nullable=False, index=True)
    owner_email = Column(String, ForeignKey("website_owners.email"), nullable=False)
    website_name = Column(String, nullable=False)
    owner = relationship("WebsiteOwner", back_populates="websites")
    scans = relationship("Scan", back_populates="website")
    
class Resource(Base):
    __tablename__ = 'resources'
    
    resource_url = Column(String, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False) 
    vulnerability = Column(String, ForeignKey('vulnerabilities.name'), nullable=False)
    vulnerabilities = relationship("Vulnerability", back_populates="resources")
    ratings = relationship("ResourceRating", back_populates="resource")


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
    ratings = relationship("CybersecurityExpertRating", back_populates="expert")

    
class Specialty(Base):
    __tablename__ = 'specialties'
    expert = Column(String, ForeignKey('cybersecurity_experts.email'), primary_key=True, nullable=False)
    vulnerability = Column(String, ForeignKey('vulnerabilities.name'), primary_key=True, nullable=False)
    cybersecurity_expert = relationship("CybersecurityExpert", back_populates="specialty")
    vulnerabilities = relationship("Vulnerability", back_populates="experts")
    
class Scan(Base):
    __tablename__ = 'scans'
    scan_id = Column(Integer, primary_key=True, nullable=False, index=True)
    website_owner = Column(String, ForeignKey('website_owners.email'), nullable=False)
    website_url = Column(String, ForeignKey('websites.url'), nullable=False)
    deep = Column(Boolean, nullable=False)
    date = Column(Date, nullable=False)
    owner = relationship("WebsiteOwner", back_populates="scans")
    website = relationship("Website", back_populates="scans")
    found_vulnerabilities = relationship("FoundVulnerability", back_populates="scans")
    
    
class Vulnerability(Base):
    __tablename__ = 'vulnerabilities'
    
    name = Column(String, primary_key=True, nullable=False, index=True)
    date_added = Column(Date, nullable=False)
    resources = relationship("Resource", back_populates="vulnerabilities")
    experts = relationship("Specialty", back_populates="vulnerabilities")
    found_scans = relationship("FoundVulnerability", back_populates="vulnerabilities")
    
class FoundVulnerability(Base):
    __tablename__ = 'found_vulnerabilities'
    scan_id = Column(Integer, ForeignKey('scans.scan_id'), primary_key=True, nullable=False)
    vulnerability = Column(String, ForeignKey('vulnerabilities.name'), primary_key=True, nullable=False)
    vulnerabilities = relationship("Vulnerability", back_populates="found_scans")
    scans = relationship("Scan", back_populates="found_vulnerabilities")
    
class ResourceRating(Base):
    __tablename__ = 'resouce_ratings'
    website_owner = Column(String, ForeignKey('website_owners.email'), primary_key=True, nullable=False)
    resource_url = Column(String, ForeignKey('resources.resource_url'), primary_key=True, nullable=False)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'), nullable=False)
    resource = relationship("Resource", back_populates="ratings")
    owner = relationship("WebsiteOwner", back_populates="resource_ratings")
    
class CybersecurityExpertRating(Base):
    __tablename__ = 'cybersecurity_expert_ratings'
    website_owner = Column(String, ForeignKey('website_owners.email'), primary_key=True, nullable=False)
    cybersecurity_expert = Column(String, ForeignKey('cybersecurity_experts.email'), primary_key=True, nullable=False)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'), nullable=False)
    expert = relationship("CybersecurityExpert", back_populates="ratings")
    owner = relationship("WebsiteOwner", back_populates="cybersecurity_expert_ratings")
    