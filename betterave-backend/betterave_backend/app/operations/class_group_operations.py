from typing import Any
from sqlalchemy.exc import SQLAlchemyError
from betterave_backend.extensions import db
from betterave_backend.app.decorators import with_instance
from betterave_backend.app.models.class_group import ClassGroup
from betterave_backend.app.models.user import User


def add_class_group(name: str, class_id: int, is_main_group: bool) -> int:
    """
    Add a class group to the database.

    Args:
        class_id (int): The ID of the class this group belongs to.
        is_main_group (bool): Indicates if this is the main group for the class.

    Returns:
        int: The ID of the newly created class group, or -1 if an error occurs.
    """
    try:
        new_group = ClassGroup(name=name, class_id=class_id, is_main_group=is_main_group)
        db.session.add(new_group)
        db.session.commit()
        return new_group.group_id  # type: ignore
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding class group: {str(e)}")
        return -1


@with_instance(ClassGroup)
def update_class_group(group: ClassGroup, new_data: dict[str, Any]) -> bool:
    """
    Modify class group information in the database.

    Args:
        group_id (int): The ID of the class group to be modified.
        new_data (dict): A dictionary containing the updated class group information.

    Returns:
        bool: True if the class group was successfully modified, False otherwise.
    """
    try:
        for key, value in new_data.items():
            if hasattr(group, key):
                setattr(group, key, value)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error modifying class group: {str(e)}")
        return False


@with_instance(ClassGroup)
def delete_class_group(group: ClassGroup) -> bool:
    """
    Remove a class group from the database.

    Args:
        group_id (int): The ID of the class group to be removed.

    Returns:
        bool: True if the class group was successfully removed, False otherwise.
    """
    try:
        db.session.delete(group)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error deleting class group: {str(e)}")
        return False


def get_class_group_by_id(group_id: int) -> ClassGroup:
    """
    Get a class group by its ID.

    Args:
        group_id (int): The ID of the class group.

    Returns:
        ClassGroup: The class group object.
    """
    return db.session.get(ClassGroup, group_id)


def get_all_class_groups() -> list[ClassGroup]:
    """
    Return all class groups in the database.

    Returns:
        list[ClassGroup]: A list of class group objects.
    """
    return ClassGroup.query.all()  # type: ignore


@with_instance([User, ClassGroup])
def enroll_student_in_group(student: User, group: ClassGroup) -> bool:
    """
    Enroll a student in a class group.

    Args:
        student (User): The student to be enrolled.
        group (ClassGroup): The class group.

    Returns:
        bool: True if the enrollment was successful, False otherwise.
    """
    try:
        if student and group:
            group.students.append(student)
            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error enrolling student: {str(e)}")
        return False


@with_instance([User, ClassGroup])
def unenroll_student_from_group(student: User, group: ClassGroup) -> bool:
    """
    Unenroll a student from a class group.

    Args:
        student (User): The student to be unenrolled.
        group (ClassGroup): The class group.

    Returns:
        bool: True if the unenrollment was successful, False otherwise.
    """
    try:
        if student and group:
            group.students.remove(student)
            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error unenrolling student: {str(e)}")
        return False


def get_class_group_by_name(class_id: int, name: str) -> ClassGroup:
    """Return a class group by its name."""
    return ClassGroup.query.filter_by(class_id=class_id, name=name).first()
