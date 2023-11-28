from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, CheckConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
    
class WebsiteOwner(Base):
    __tablename__ = 'website_owners'
    
    email = Column(String, primary_key=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    websites = relationship("Website", back_populates="owner")
    scans = relationship("Scan", back_populates="owner")
    resource_ratings = relationship("ResourceRating", back_populates="owner")
    cybersecurity_expert_ratings = relationship("CybersecurityExpertRating", back_populates="owner")
    cybersecurity_expert_messages = relationship("Message", back_populates="owner")
    cookie = relationship("Cookie", back_populates="owner", uselist=False)

    
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


class IssuedCertification(Base):
    __tablename__ = 'issued_certifications'
    image = Column(String, primary_key=True, nullable=False)
    recipient = Column(String, ForeignKey('cybersecurity_experts.email'), primary_key=True, nullable=False)
    expert = relationship("CybersecurityExpert", back_populates="certifications")

class CybersecurityExpert(Base):
    __tablename__ = 'cybersecurity_experts'
    
    email = Column(String, primary_key=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    certifications = relationship("IssuedCertification", back_populates="expert")
    specialty = relationship("Specialty", back_populates="cybersecurity_expert")
    ratings = relationship("CybersecurityExpertRating", back_populates="expert")
    messages = relationship("Message", back_populates="expert")

    
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
    tested_vulnerabilities = relationship("TestedVulnerability", back_populates="scans")
    
    
class Vulnerability(Base):
    __tablename__ = 'vulnerabilities'
    
    name = Column(String, primary_key=True, nullable=False, index=True)
    date_added = Column(Date, nullable=False)
    resources = relationship("Resource", back_populates="vulnerabilities")
    experts = relationship("Specialty", back_populates="vulnerabilities")
    tested_scans = relationship("TestedVulnerability", back_populates="vulnerabilities")
    
class TestedVulnerability(Base):
    __tablename__ = 'tested_vulnerabilities'
    scan_id = Column(Integer, ForeignKey('scans.scan_id'), primary_key=True, nullable=False)
    vulnerability = Column(String, ForeignKey('vulnerabilities.name'), primary_key=True, nullable=False)
    score = Column(Integer, CheckConstraint('score >= 0 AND score <= 100'), nullable=True)
    success = Column(Boolean, nullable=False)
    description = Column(String, nullable=True)
    vulnerabilities = relationship("Vulnerability", back_populates="tested_scans")
    scans = relationship("Scan", back_populates="tested_vulnerabilities")
    
class ResourceRating(Base):
    __tablename__ = 'resouce_ratings'
    website_owner = Column(String, ForeignKey('website_owners.email'), primary_key=True, nullable=False)
    resource_url = Column(String, ForeignKey('resources.resource_url'), primary_key=True, nullable=False)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'), nullable=True)
    resource = relationship("Resource", back_populates="ratings")
    owner = relationship("WebsiteOwner", back_populates="resource_ratings")
    
class CybersecurityExpertRating(Base):
    __tablename__ = 'cybersecurity_expert_ratings'
    website_owner = Column(String, ForeignKey('website_owners.email'), primary_key=True, nullable=False)
    cybersecurity_expert = Column(String, ForeignKey('cybersecurity_experts.email'), primary_key=True, nullable=False)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'), nullable=True)
    expert = relationship("CybersecurityExpert", back_populates="ratings")
    owner = relationship("WebsiteOwner", back_populates="cybersecurity_expert_ratings")
    
class Message(Base):
    __tablename__ = 'messages'
    website_owner = Column(String, ForeignKey('website_owners.email'), primary_key=True, nullable=False)
    cybersecurity_expert = Column(String, ForeignKey('cybersecurity_experts.email'), primary_key=True, nullable=False)
    payload = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
    time_sent = Column(DateTime, nullable=False)
    expert = relationship("CybersecurityExpert", back_populates="messages")
    owner = relationship("WebsiteOwner", back_populates="cybersecurity_expert_messages")

    
class Cookie(Base):
    __tablename__ = 'cookies'
    cookie_value = Column(String, primary_key=True, nullable=False)
    email = Column(String, ForeignKey("website_owners.email"), nullable=False)
    owner = relationship("WebsiteOwner", back_populates="cookie")
    