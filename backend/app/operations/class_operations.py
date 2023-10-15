from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from app.models.class_ import Class
from app.models.user import User
from app.operations.user_operations import get_user_by_id

def add_class(class_id, name, ects_credits, default_teacher_id, backgroundColor, **kwargs) -> int:
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
            backgroundColor=backgroundColor,
        )

        db.session.add(new_class)
        db.session.commit()
        return class_id
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding class: {str(e)}")
        return -1

def modify_class(class_id, new_data: dict) -> bool:
    """
    Modify class information in the database.

    Args:
        class_id (int): The ID of the class to be modified.
        new_data (dict): A dictionary containing the updated class information.

    Returns:
        bool: True if the class was successfully modified, False otherwise.
    """
    try:
        class_ = get_class_by_id(class_id)
        if class_:
            for key, value in new_data.items():
                if hasattr(class_, key):
                    setattr(class_, key, value)

            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error modifying class: {str(e)}")
        return False

def remove_class(class_id: int) -> bool:
    """
    Remove a class from the database.

    Args:
        class_id (int): The ID of the class to be removed.

    Returns:
        bool: True if the class was successfully removed, False otherwise.
    """
    try:
        class_ = get_class_by_id(class_id)
        if class_:
            db.session.delete(class_)
            db.session.commit()
            return True
        return False
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

def authorize_teacher_for_class(teacher_id: int, class_id: int) -> bool:
    """
    Authorize a teacher for a specific class.

    Args:
        teacher_id (int): The ID of the teacher user.
        class_id (int): The ID of the class.

    Returns:
        bool: True if the operation is successful, False otherwise.
    """
    try:
        # Retrieve the class and user instances
        target_class = get_class_by_id(class_id)
        teacher = get_user_by_id(teacher_id)

        # If either is not found, return False
        if not target_class or not teacher:
            return False

        # If the teacher is already authorized, no need to proceed
        if teacher in target_class.authorized_teachers:
            return True

        # Authorize the teacher for the class
        target_class.authorized_teachers.append(teacher)
        
        db.session.commit()

        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error authorizing teacher for class: {str(e)}")
        return False

def get_authorized_teachers_for_class(class_id: int) -> list[User]:
    """
    Retrieve all authorized teachers for a specific class.

    Args:
        class_id (int): The ID of the class.

    Returns:
        List[User]: A list of User objects representing the authorized teachers.
    """
    target_class = Class.query.get(class_id)
    if not target_class:
        return []

    return target_class.authorized_teachers

def deauthorize_teacher_for_class(teacher_id: int, class_id: int) -> bool:
    """
    Deauthorize a teacher for a specific class.

    Args:
        teacher_id (int): The ID of the teacher user.
        class_id (int): The ID of the class.

    Returns:
        bool: True if the operation is successful, False otherwise.
    """
    try:
        target_class = Class.query.get(class_id)
        teacher = User.query.get(teacher_id)

        if not target_class or not teacher:
            return False

        if teacher in target_class.authorized_teachers:
            target_class.authorized_teachers.remove(teacher)
        
        db.session.commit()

        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error deauthorizing teacher for class: {str(e)}")
        return False
