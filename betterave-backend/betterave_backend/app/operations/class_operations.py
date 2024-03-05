# type: ignore
import time
from sqlalchemy.exc import SQLAlchemyError
from betterave_backend.extensions import db
from betterave_backend.app.models import UserLevel, Class, ClassGroup, Lesson
from betterave_backend.app.decorators import with_instance


def add_class(class_id, name, ects_credits, default_teacher_id, level, background_color, **kwargs) -> int:
    """
    Add a class to the database.

    Args:
        class_id (int): The ID of the class.
        name (str): The name of the class.
        ects_credits (int): The ECTS credits for the class.
        default_teacher_id (int): The default teacher for the class.
        background_color (str): The background color for the class.
        **kwargs: Additional class attributes (e.g., ensae_link).

    Returns:
        int: The ID of the newly created class.
    """
    try:
        ensae_link = kwargs.get("ensae_link", f"https://www.ensae.fr/courses/{class_id}")

        new_class = Class(
            class_id=class_id,
            name=name,
            ects_credits=ects_credits,
            ensae_link=ensae_link,
            default_teacher_id=default_teacher_id,
            level=UserLevel(level.upper()) if isinstance(level, str) else level,
            background_color=background_color,
        )

        db.session.add(new_class)
        db.session.commit()
        return class_id
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding class: {str(e)}")
        return -1


@with_instance(Class)
def update_class(class_instance: Class, new_data: dict) -> bool:
    """
    Update class information in the database.

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
def delete_class(class_instance: Class) -> bool:
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


def get_classes_from_teacher(teacher_id: int) -> list:
    """Return all classes of a given teacher id."""
    # Being the teacher of a Lesson of the class is enough to be considered the teacher of a class.
    # Classes have Classes.groups, and ClassGroup have ClassGroup.lessons.
    # We also include the default teacher of the class.
    start_time = time.time()
    default_teacher_classes = Class.query.filter_by(default_teacher_id=teacher_id).all()
    lesson_classes = (
        Class.query.join(Class.groups).join(ClassGroup.lessons).filter(Lesson.teacher_id == teacher_id).all()
    )
    print(f"get_classes_from_teacher took {time.time() - start_time} seconds", flush=True)
    return list(set(default_teacher_classes + lesson_classes))
