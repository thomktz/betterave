from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from app.models import Homework
from app.decorators import with_instance

def add_homework(homework_id, title) -> int:
    """
    Add a homework to the database.

    Args:
        homework_id (int): The ID of the homework.
        title (str): The name of the homework.

    Returns:
        int: The ID of the newly created homework.
    """
    try:
        
        new_homework = Homework(
            homework_id=homework_id,
            title=title,
        )

        db.session.add(new_homework)
        db.session.commit()
        return homework_id
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding homewor: {str(e)}")
        return -1

@with_instance(Homework)
def update_homework(homework_instance: Homework, new_data: dict) -> bool:
    """
    Update homework in the database.

    Args:
        homework_instance (Homework): The instance of the homework to be modified.
        new_data (dict): A dictionary containing the updated homework information.

    Returns:
        bool: True if the homework was successfully modified, False otherwise.
    """
    try:
        for key, value in new_data.items():
            if hasattr(homework_instance, key):
                setattr(homework_instance, key, value)

        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error modifying homework: {str(e)}")
        return False
    
    
@with_instance(Homework)
def delete_homework(homework_instance: Homework) -> bool:
    """
    Remove a homework from the database.

    Args:
        homework_instance (Homework): The instance of the homework to be removed.

    Returns:
        bool: True if the homework was successfully removed, False otherwise.
    """
    try:
        db.session.delete(homework_instance)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error deleting homework: {str(e)}")
        return False

def get_homework_by_id(homework_id: int) -> Homework:
    """Get a homework by its ID."""
    return db.session.get(Homework, homework_id)

def get_all_homeworks() -> list:
    """Return all homeworks in the database."""
    return Homework.query.all()
