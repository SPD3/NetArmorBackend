from src import models

# Resource Functions
def check_resource(db_session, resource_url, title, vulnerability):
    resource = db_session.query(models.Resource).filter(models.Resource.resource_url==resource_url).first()
    return resource is not None and (resource.title == title and resource.vulnerability == vulnerability)

def check_sqli_resource(db_session):
    return check_resource(db_session, "https://owasp.org/www-community/attacks/SQL_Injection", "SQL Injection", "SQL Injection")

def add_resource(db_session, resource_url, title, vulnerability):
    db_resource = models.Resource(resource_url=resource_url, title=title, vulnerability=vulnerability)
    db_session.add(db_resource)
    
def add_sqli_resource(db_session):
    add_resource(db_session, "https://owasp.org/www-community/attacks/SQL_Injection", "SQL Injection", "SQL Injection")

# ResourceRating Functions
def check_resource_rating(db_session, website_owner, resource_url, rating):
    resource_rating = db_session.query(models.ResourceRating).filter(models.ResourceRating.website_owner==website_owner
                                                        and models.ResourceRating.resource_url==resource_url).first()
    return resource_rating is not None and (resource_rating.rating == rating)

def check_sqli_rating(db_session):
    return check_resource_rating(db_session, "mickey@mouse.com", "https://owasp.org/www-community/attacks/SQL_Injection", 5)

def add_resource_rating(db_session, email, resource_url, rating):
    db_resource_rating = models.ResourceRating(website_owner=email, resource_url=resource_url, rating=rating)
    db_session.add(db_resource_rating)
    
def add_sqli_rating(db_session):
    add_resource_rating(db_session, "mickey@mouse.com", "https://owasp.org/www-community/attacks/SQL_Injection", 5)