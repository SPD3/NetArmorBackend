from src import models


# Resource Functions
def check_resource(db_session, resource_url, title, vulnerability):
    resources = db_session.query(models.Resource).filter(models.Resource.resource_url==resource_url).all()
    if len(resources) != 1:
        return False
    resource = resources[0]
    return (resource.title == title and resource.vulnerability == vulnerability)

def add_resource(db_session, resource_url, title, vulnerability):
    db_resource = models.Resource(resource_url=resource_url, title=title, vulnerability=vulnerability)
    db_session.add(db_resource)