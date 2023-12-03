from src import models

# Message Functions
def check_message(db_session, website_owner, cybersecurity_expert, payload, is_pending, time_sent):
    messages = db_session.query(models.Message).filter(
                                        models.Message.website_owner==website_owner
                                        and models.Message.cybersecurity_expert==cybersecurity_expert).all()
    if len(messages) != 1:
        return False
    message = messages[0]
    return message is not None and (message.payload == payload and message.is_pending == is_pending and message.time_sent == time_sent)


def add_message(db_session, email, expert_email, payload, is_pending, time_sent):
    db_message = models.Message(website_owner=email, cybersecurity_expert=expert_email, payload=payload, is_pending=is_pending, time_sent=time_sent)
    db_session.add(db_message)