from src import models

# Website Owner Functions
def check_website_owner(db_session, email, password, first_name, last_name, image):
    website_owners = db_session.query(models.WebsiteOwner).filter(models.WebsiteOwner.email==email).all()
    if len(website_owners) != 1:
        return False
    website_owner =  website_owners[0]
    return  (website_owner.password == password
                                          and website_owner.first_name == first_name
                                          and website_owner.last_name == last_name
                                          and website_owner.image == image)
    
def add_website_owner(db_session, email, password, first_name, last_name, image):
    db_website = models.WebsiteOwner(email=email, password=password, first_name=first_name, last_name=last_name, image=image)
    db_session.add(db_website)
    

# Website Functions
def check_website(db_session, url, owner_email, website_name):
    websites = db_session.query(models.Website).filter(models.Website.url==url).all()
    if len(websites) != 1:
        return False
    website = websites[0]
    return website is not None and website.owner_email == owner_email and website.website_name == website_name

def add_website(db_session, url, owner_email, website_name):
    db_website = models.Website(url=url, owner_email=owner_email, website_name=website_name)
    db_session.add(db_website)
    