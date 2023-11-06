from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from app.models import UserLevel, Class
from app.decorators import with_instance

def add_class(class_id, name, ects_credits, default_teacher_id, level, backgroundColor, **kwargs) -> int:
    """
    Add a class to the database.

    Args:
        class_id (int): The ID of the class.
        name (str): The name of the class.
        ects_credits (int): The ECTS credits for the class.
        default_teacher_id (int): The default teacher for the class.
        backgroundColor (str): The background color for the class.
        **kwargs: Additional class attributes (e.g., ensae_link).

    Returns:
        int: The ID of the newly created class.
    """
    try:
        ensae_link = kwargs.get('ensae_link', f"https://www.ensae.fr/courses/{class_id}")
        
        new_class = Class(
            class_id=class_id,
            name=name,
            ects_credits=ects_credits,
            ensae_link=ensae_link,
            default_teacher_id=default_teacher_id,
            level=UserLevel(level.upper()) if isinstance(level, str) else level,
            backgroundColor=backgroundColor,
        )

        db.session.add(new_class)
        db.session.commit()
        return class_id
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding class: {str(e)}")
        return -1

@with_instance(Class)
def modify_class(class_instance: Class, new_data: dict) -> bool:
    """
    Modify class information in the database.

    Args:
        class_instance (Class): The instance of the class to be modified.
        new_data (dict): A dictionary containing the updated class information.

    Returns:
        bool: True if the class was successfully modified, False otherwise.
    """
    try:
        for key, value in new_data.items():
            if hasattr(class_instance, key):
                setattr(class_instance, key, value)

        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error modifying class: {str(e)}")
        return False
    
    
@with_instance(Class)
def remove_class(class_instance: Class) -> bool:
    """
    Remove a class from the database.

    Args:
        class_instance (Class): The instance of the class to be removed.

    Returns:
        bool: True if the class was successfully removed, False otherwise.
    """
    try:
        db.session.delete(class_instance)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error deleting class: {str(e)}")
        return False

def get_class_by_id(class_id: int) -> Class:
    """Get a class by its ID."""
    return db.session.get(Class, class_id)

def get_all_classes() -> list:
    """Return all classes in the database."""
    return Class.query.all()

def get_classes_from_level(level: UserLevel) -> list:
    """Return all classes of a given level."""
    return Class.query.filter_by(level=level).all()