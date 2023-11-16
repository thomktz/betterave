from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from app.models import Homework, Class
from app.decorators import with_instance
from app.operations.class_operations import get_class_by_id

def get_homeworks_by_group_id(group_id: int):
    """Retrieve homeworks for a specific class."""
    return Homework.query.filter_by(group_id=group_id).all()

def add_homework_to_group(content: str, group_id: int, homework_id: int, due_date):
    """Add a homework to a specific class."""
    hmw = Homework(content=content, group_id=group_id, homework_id=homework_id, due_date=due_date)
    db.session.add(hmw)
    db.session.commit()

    print(hmw.as_dict(), flush=True)
    
    return hmw

@with_instance(Homework)
def delete_homework(homework: Homework):
    """Delete a homework."""
    if homework:
        db.session.delete(homework)
        db.session.commit()
        return True
    return False

@with_instance(Class)
def get_class_homeworks(class_: Class):
    """Retrieve homeworks for a specific class."""
    return get_homeworks_by_group_id(class_.main_group().group_id)

    
def add_class_homework(content, class_id, homework_id, due_date):
    """Add a homework to a specific class's main group."""
    class_ = get_class_by_id(class_id)
    if class_ and class_.main_group():
        # Add homework to the main group of the class.
        return add_homework_to_group(content, class_.main_group().group_id, homework_id,due_date)
    else:
        # Handle the case where the class or main group doesn't exist.
        return None
