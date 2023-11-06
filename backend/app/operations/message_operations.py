from extensions import db
from app.decorators import with_instance
from app.models import Message, Class
from app.operations.class_operations import get_class_by_id


def get_group_messages(group_id: int):
    """Retrieve messages for a specific class."""
    return Message.query.filter_by(group_id=group_id).all()

def add_group_message(content: str, group_id: int, user_id: int):
    """Add a message to a specific class."""
    msg = Message(content=content, group_id=group_id, user_id=user_id)
    db.session.add(msg)
    db.session.commit()
    return msg

@with_instance(Class)
def get_class_messages(class_: Class):
    """Retrieve messages for a specific class."""
    return get_group_messages(class_.main_group().group_id)

    
def add_class_message(content, class_id, user_id):
    """Add a message to a specific class's main group."""
    class_ = get_class_by_id(class_id)
    if class_ and class_.main_group():
        # Add message to the main group of the class.
        return add_group_message(content, class_.main_group().group_id, user_id)
    else:
        # Handle the case where the class or main group doesn't exist.
        return None
