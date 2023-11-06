from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from app.models import UserClassGroup, ClassGroup
from app.decorators import with_instance


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
def modify_user_class_group(user_class_group: UserClassGroup, new_data: dict) -> bool:
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