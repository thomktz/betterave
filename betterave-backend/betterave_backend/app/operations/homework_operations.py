from datetime import datetime
from betterave_backend.extensions import db
from betterave_backend.app.models import Homework, Class, User
from betterave_backend.app.decorators import with_instance
from betterave_backend.app.operations.class_operations import get_class_by_id


def get_homework_by_group_id(group_id: int) -> list[Homework]:
    """Retrieve homework for a specific class."""
    return sorted(Homework.query.filter_by(group_id=group_id).all())


def add_homework_to_group(content: str, due_date: str, due_time: str, group_id: int) -> Homework:
    """Add a homework to a specific class."""
    date = datetime.strptime(due_date, "%Y-%m-%d").date()
    time = datetime.strptime(due_time, "%H:%M").time() if due_time else None
    hmw = Homework(content=content, group_id=group_id, due_date=date, due_time=time)
    db.session.add(hmw)
    db.session.commit()
    return hmw


@with_instance(Homework)
def delete_homework(homework: Homework) -> bool:
    """Delete a homework."""
    if homework:
        db.session.delete(homework)
        db.session.commit()
        return True
    return False


@with_instance(Class)
def get_class_homework(class_: Class) -> list[Homework]:
    """Retrieve homework for a specific class."""
    return get_homework_by_group_id(class_.main_group().group_id)


def add_homework_to_class(content: str, class_id: int, due_date: str, due_time: str) -> Homework:
    """Add a homework to a specific class's main group."""
    class_ = get_class_by_id(class_id)
    if class_ and class_.main_group():
        # Add homework to the main group of the class.
        return add_homework_to_group(content, due_date, due_time, class_.main_group().group_id)
    else:
        # Handle the case where the class or main group doesn't exist.
        return None


@with_instance(User)
def get_user_homework(user: User) -> list[Homework]:
    """Get all homework for a specific user."""
    all_homework = []
    for ucg in user.class_groups:
        all_homework += get_homework_by_group_id(ucg.primary_class_group.group_id)
    return sorted(all_homework)
