from src import models

# Website Owner Functions
def check_website_owner(db_session, email, password, first_name, last_name):
    website_owner = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email==email).first()
    return website_owner is not None and (website_owner.password == password
                                          and website_owner.first_name == first_name
                                          and website_owner.last_name == last_name)

def check_mickey(db_session):
    return check_website_owner(db_session, "mickey@mouse.com", "12345", "Mickey", "Mouse")
    
def add_website_owner(db_session, email, password, first_name, last_name):
    db_website = models.WebsiteOwner(email=email, password=password, first_name=first_name, last_name=last_name)
    db_session.add(db_website)
    
def add_mickey(db_session):
    add_website_owner(db_session, "mickey@mouse.com", "12345", "Mickey", "Mouse")

# Website Owner Functions
def check_website_owner(db_session, email, password, first_name, last_name):
    website_owner = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email==email).first()
    return website_owner is not None and (website_owner.password == password
                                          and website_owner.first_name == first_name
                                          and website_owner.last_name == last_name)

def check_mickey(db_session):
    return check_website_owner(db_session, "mickey@mouse.com", "12345", "Mickey", "Mouse")
    
def add_website_owner(db_session, email, password, first_name, last_name):
    db_website = models.WebsiteOwner(email=email, password=password, first_name=first_name, last_name=last_name)
    db_session.add(db_website)
    
def add_mickey(db_session):
    add_website_owner(db_session, "mickey@mouse.com", "12345", "Mickey", "Mouse")

# Website Functions
def check_website(db_session, url, owner_email, website_name):
    website = db_session.query(models.Website).filter(models.Website.url==url).first()
    return website is not None and website.owner_email == owner_email and website.website_name == website_name

def check_mickey_website(db_session):
    return check_website(db_session, "mickeymousewebsite.com", "mickey@mouse.com", "Mickey's Website")

def add_website(db_session, url, owner_email, website_name):
    db_website = models.Website(url=url, owner_email=owner_email, website_name=website_name)
    db_session.add(db_website)
    
def add_mickey_website(db_session):
    add_website(db_session, "mickeymousewebsite.com", "mickey@mouse.com", "Mickey's Website")