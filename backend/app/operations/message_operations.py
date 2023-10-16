from extensions import db
from app.models import Message

def get_class_messages(class_id):
    """Retrieve messages for a specific class."""
    return Message.query.filter_by(class_id=class_id).order_by(Message.timestamp).all()

def add_class_message(content, class_id, user_id):
    """Add a message to a specific class."""
    msg = Message(content=content, class_id=class_id, user_id=user_id)
    db.session.add(msg)
    db.session.commit()
    return msg