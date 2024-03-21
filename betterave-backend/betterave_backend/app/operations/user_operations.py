"""
This module contains functions for performing operations on users in the database.

It excludes operations related specifically to students, which are defined in student_operations.py.
"""
from typing import Optional, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from betterave_backend.extensions import db, bcrypt
from betterave_backend.app.decorators import with_instance
from betterave_backend.app.models import UserLevel, UserType, User
from betterave_backend.app.operations.event_operations import get_all_events
from betterave_backend.app.operations.notification_operations import get_all_notifications


def create_register_hash(name: str, surname: str, key: str = "ENSAE2024"):
    """
    Create the code needed upon account creation.

    These would be sent to students via email when their enrollment is confirmed.
    To make this even more secure, we could add information known to us and the student, but not outsiders.
    For example, we could add the INE number of the student inside the hash and ask for the INE on register as well.
    This way, even if someone were to intercept the hash, they couldn't register.

    In practice, 'key' would be randomly generated once for all students of that year.
    """
    return bcrypt.generate_password_hash((name + surname + key).lower()).decode("utf-8")


def check_register_hash(hash: str, name: str, surname: str, key: str = "ENSAE2024"):
    """Check that the register hash matches the student's information."""
    # Disable the actual checking
    if False:
        return bcrypt.check_password_hash(hash, create_register_hash(name, surname, key))

    # For the purpose of this project, we will omit the actual hash
    # and use a common string, for simplicity.
    return hash == "3N543"  # ('ENSAE')


def hash_password(password: str) -> str:
    """Hash a given password."""
    return bcrypt.generate_password_hash(password).decode("utf-8")


def check_password(hashed_password: str, password: str) -> bool:
    """Check if a given password matches a hashed password."""
    return bcrypt.check_password_hash(hashed_password, password)


def authenticate_user(email: str, password: str) -> bool:
    """Authenticate a user using their email and password."""
    user = get_user_by_email(email.lower())
    if not user:
        return False
    return check_password(user.hashed_password, password)


def add_user(
    name: str,
    surname: str,
    profile_pic: str,
    user_type: str,
    level: str = "N/A",
    register_hash: str = "3N543",  # There would never be a default value in production, of course.
    email_override: Optional[str] = None,
    password_override: Optional[str] = None,
    linkedin: Optional[str] = None,
    website: Optional[str] = None,
) -> int:
    """
    Add a user to the database.

    Args:
        name (str): The user's first name.
        surname (str): The user's last name.
        profile_pic (str): URL to the user's profile picture.
        level (str): The user's level or grade.
        user_type (str): The type of user ('student', 'student_asso', 'teacher', 'admin').
        register_hash (str): The code sent to the student via email.
        email_override (str, optional): The user's email address. Defaults to None.
        linkedin (str, optional): The user's LinkedIn profile URL. Defaults to None.
        website (str, optional): The user's personal website URL. Defaults to None.

    Returns:
        int: The ID of the newly created user, or -1 if an error occurs.
    """
    try:
        if not check_register_hash(register_hash, name, surname):
            return -1
        if email_override:
            email = email_override
            password = email_override.split("@")[0]  # Take the part before the @ as password
        else:
            email = f"{name.lower()}.{surname.replace(' ', '-').lower()}@ensae.fr"
            password = f"{name[0].lower()}{surname.replace(' ', '-').lower()}"
        if password_override:
            password = password_override
        hashed_password = hash_password(password)
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            name=name,
            surname=surname,
            profile_pic=profile_pic,
            user_type=UserType(user_type),
            level=UserLevel(level),
            linkedin=linkedin,
            website=website,
        )

        # Add the user to the session first
        db.session.add(new_user)
        db.session.commit()

        # Update the user's attendance to events
        update_event_attendance(new_user)
        
        # Update the user's reception of notifications
        update_notifications(new_user)

        return new_user.user_id
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding user: {str(e)}")
        return -1


@with_instance(User)
def update_event_attendance(user: User) -> None:
    """Update the attendance of a user to the events of the database."""
    # Loop through all events
    for event in get_all_events():
        # If user already has an attendance for this event
        if event in user.attended_events:
            if event.participant_type == "Subscribers" and event.association not in user.subscriptions:
                user.attended_events.remove(event)

            elif event.participant_type == "All users":
                continue

            if event.participant_type != user.level.value:
                user.attended_events.remove(event)
            continue

        # If not, should the user be added to the event?
        if event.participant_type == "Subscribers":
            if event.association in user.subscriptions:
                user.attended_events.append(event)

        elif event.participant_type == "All users":
            user.attended_events.append(event)

        elif event.participant_type == user.level.value:
            user.attended_events.append(event)

    db.session.commit()
    
    
@with_instance(User)
def update_notifications(user: User) -> None:
    """Update the reception of a user to the notifications of the database."""
    # Loop through all notifications
    for notif in get_all_notifications():
        # If user already has an attendance for this event
        if notif in user.attended_events:
            if notif.recipient_type == "Subscribers" and notif.association not in user.subscriptions:
                user.receptionned_notifications.remove(notif)

            elif notif.recipient_type == "All users":
                continue

            if notif.recipient_type != user.level.value:
                user.receptionned_notifications.remove(notif)
            continue

        # If not, should the user be added to the event?
        if notif.recipient_type == "Subscribers":
            if notif.association in user.subscriptions:
                user.receptionned_notifications.append(notif)

        elif notif.recipient_type == "All users":
            user.receptionned_notifications.append(notif)

        elif notif.recipient_type == user.level.value:
            user.receptionned_notifications.append(notif)

    db.session.commit()


@with_instance(User)
def update_user(user: User, new_data: dict[str, Any]) -> bool:
    """
    Modify user information in the database.

    Args:
        user_id (int): The ID of the user to be modified.
        new_data (dict): A dictionary containing the updated user information.

    Returns:
        bool: True if the user was successfully modified, False otherwise.
    """
    try:
        reset_class_groups = False
        for key, value in new_data.items():
            if hasattr(user, key):
                if key == "level":
                    value = UserLevel(value)
                    reset_class_groups = True
                elif key == "user_type":
                    value = UserType(value)
                setattr(user, key, value)
        if reset_class_groups:
            for ucg in user.class_groups:
                db.session.delete(ucg)
            user.class_groups = []
            user.groups = []
        db.session.commit()

        # Update the user's attendance to events
        update_event_attendance(user)
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error modifying user: {str(e)}")
        return False


@with_instance(User)
def delete_user(user: User) -> bool:
    """
    Remove a user from the database.

    Args:
        user_id (int): The ID of the user to be removed.

    Returns:
        bool: True if the user was successfully removed, False otherwise.
    """
    try:
        # Delete all UserClassGroup associations
        for ucg in user.class_groups:
            db.session.delete(ucg)

        db.session.delete(user)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error deleting user: {str(e)}")
        return False


def get_user_by_id(user_id: int) -> User:
    """Get a user by their ID."""
    return db.session.get(User, user_id)


def get_user_by_email(email: str) -> User:
    """Get a user by their email."""
    return User.query.filter_by(email=email).first()


def get_all_users() -> list[User]:
    """Return all users in the database."""
    return User.query.all()


@with_instance(User)
def get_user_profile_pic(user: User) -> str:
    """Get the profil picture of a particular user."""
    return user.profile_pic


def get_user_by_name(name: str, surname: str) -> User:
    """Get a user by their name and surname."""
    user = User.query.filter(and_(User.name.ilike(name), User.surname.ilike(surname))).first()
    if user:
        return user
    raise ValueError(f"User {name} {surname} not found")
