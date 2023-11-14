from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from app.models import UserClassGroup, ClassGroup
from app.decorators import with_instance
from app.operations.class_group_operations import enroll_student_in_group, unenroll_student_from_group

def enroll_user_in_class(user_id: int, class_id: int):
    """
    Enroll a user in a class.

    Args:
        user_id (int): The ID of the user (student).
        class_id (int): The ID of the class.

    Returns:
        bool: True if the user was successfully enrolled, False otherwise.
    """
    # Check if the user is already enrolled in the class
    if ucg := get_ucg_by_user_and_class(user_id, class_id):
        return "Already enrolled in class", ucg.id

    # Get the main group for the class
    main_group = ClassGroup.query.filter_by(class_id=class_id, is_main_group=True).first()
    if not main_group:
        return "Class has no main group", None
    
    # Pick the secondary groups which has the lowest number of students
    secondary_groups = ClassGroup.query.filter_by(class_id=class_id, is_main_group=False).all()
    secondary_groups.sort(key=lambda x: len(x.students))
    secondary_group = secondary_groups[0] if secondary_groups else None

    # Enroll student in groups
    enroll_student_in_group(user_id, main_group.group_id)
    if secondary_group:
        enroll_student_in_group(user_id, secondary_group.group_id)
        
    # Create a new UserClassGroup
    if ucg_id := add_user_class_group(
        user_id=user_id,
        class_id=class_id,
        primary_class_group_id=main_group.group_id,
        secondary_class_group_id=secondary_group.group_id if secondary_group else None
    ):
        return "Success", ucg_id
    else:
        return "Error adding user to class", None
    
def unenroll_user_from_class(user_id: int, class_id: int):
    """
    Unenroll a user from a class.

    Args:
        user_id (int): The ID of the user (student).
        class_id (int): The ID of the class.

    Returns:
        bool: True if the user was successfully unenrolled, False otherwise.
    """
    # Get the UserClassGroup
    user_class_group = get_ucg_by_user_and_class(user_id, class_id)
    if not user_class_group:
        return "Not enrolled in class"

    # Unenroll student from groups
    unenroll_student_from_group(user_id, user_class_group.primary_class_group)
    if user_class_group.secondary_class_group:
        unenroll_student_from_group(user_id, user_class_group.secondary_class_group)

    # Delete the UserClassGroup
    if delete_user_class_group(user_class_group):
        return "Success"
    else:
        return "Error deleting user from class"

def add_user_class_group(user_id: int, class_id: int, primary_class_group_id: int, secondary_class_group_id: int = None) -> int:
    """
    Add a UserClassGroup to the database.

    Args:
        user_id (int): The ID of the user (student).
        class_id (int): The ID of the class.
        primary_class_group_id (int): The ID of the primary class group.
        secondary_class_group_id (int, optional): The ID of the secondary class group, if any.

    Returns:
        int: The ID of the newly created UserClassGroup, or -1 if an error occurs.
    """
    try:
        new_user_class_group = UserClassGroup(
            user_id=user_id,
            class_id=class_id,
            primary_class_group_id=primary_class_group_id,
            secondary_class_group_id=secondary_class_group_id
        )
        db.session.add(new_user_class_group)
        db.session.commit()
        return new_user_class_group.id
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding user class group: {str(e)}")
        return -1


@with_instance(UserClassGroup)
def update_user_class_group(user_class_group: UserClassGroup, new_data: dict) -> bool:
    """
    Modify UserClassGroup information in the database.

    Args:
        user_class_group (UserClassGroup): The UserClassGroup instance to be modified.
        new_data (dict): A dictionary containing the updated information.

    Returns:
        bool: True if the UserClassGroup was successfully modified, False otherwise.
    """
    try:
        # Check if secondary_class_group_id is about to be changed
        new_secondary_group_id = new_data.get('secondary_class_group_id')
        if new_secondary_group_id and new_secondary_group_id != user_class_group.secondary_class_group_id:
            # Step 1: Remove the user from the old group
            old_group = ClassGroup.query.get(user_class_group.secondary_class_group_id)
            if old_group:
                old_group.students.remove(user_class_group.user)

            # Update the user_class_group
            user_class_group.secondary_class_group_id = new_secondary_group_id

            # Step 3: Add the user to the new group
            new_group = ClassGroup.query.get(new_secondary_group_id)
            if new_group:
                new_group.students.append(user_class_group.user)

        else:
            # Update other modifiable attributes
            for key, value in new_data.items():
                if hasattr(user_class_group, key):
                    setattr(user_class_group, key, value)

        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error modifying user class group: {str(e)}")
        return False



@with_instance(UserClassGroup)
def delete_user_class_group(user_class_group: UserClassGroup) -> bool:
    """
    Remove a UserClassGroup from the database.

    Args:
        user_class_group (UserClassGroup): The UserClassGroup instance to be removed.

    Returns:
        bool: True if the UserClassGroup was successfully removed, False otherwise.
    """
    try:
        db.session.delete(user_class_group)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error deleting user class group: {str(e)}")
        return False


def get_user_class_group_by_id(user_class_group_id: int) -> UserClassGroup:
    """
    Get a UserClassGroup by its ID.

    Args:
        user_class_group_id (int): The ID of the UserClassGroup.

    Returns:
        UserClassGroup: The UserClassGroup instance.
    """
    return db.session.get(UserClassGroup, user_class_group_id)

def get_ucg_by_user_and_class(user_id: int, class_id: int) -> UserClassGroup:
    """
    Get a UserClassGroup by its user ID and class ID.

    Args:
        user_id (int): The ID of the user.
        class_id (int): The ID of the class.

    Returns:
        UserClassGroup: The UserClassGroup instance.
    """
    return UserClassGroup.query.filter_by(user_id=user_id, class_id=class_id).first()