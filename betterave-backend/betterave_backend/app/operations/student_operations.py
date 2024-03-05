from betterave_backend.app.decorators import with_instance
from betterave_backend.app.models import User, ClassGroup, Class, UserType, UserLevel


@with_instance(User)
def get_student_groups(user: User) -> list[ClassGroup]:
    """Get all class groups a student is enrolled in."""
    return user.groups  # type: ignore


def get_all_students() -> list[User]:
    """Return all student users in the database."""
    # Assuming UserType is an enum and "student" is one of its members
    return User.query.filter(User.user_type == UserType.STUDENT).all()  # type: ignore


def get_students_from_level(level: UserLevel) -> list[User]:
    """Return all student users from a specific level."""
    return User.query.filter(User.user_type == UserType.STUDENT, User.level == level).all()  # type: ignore


@with_instance([User, ClassGroup])
def is_student_in_group(student: User, group: ClassGroup) -> bool:
    """Check if a student is in a specific class group."""
    return student in group.students


@with_instance([User, Class])
def is_student_in_class(student: User, class_: Class) -> bool:
    """
    Check if a student is in the main group of a specific class.

    Args:
        student_id (int): The ID of the student.
        class_id (int): The ID of the class.

    Returns:
        bool: True if the student is in the main group of the class, False otherwise.
    """
    return student in class_.main_group().students


def get_students_from_class(class_id: int) -> list[User]:
    """
    Get all students who have taken a specific class.

    Args:
        class_id (int): The ID of the class.

    Returns:
        List[User]: List of students who have taken the class.
    """
    # Récupérez l'objet Class correspondant à class_id
    class_ = Class.query.get(class_id)

    # Vérifiez si la classe existe
    if class_:
        # Récupérez tous les étudiants du groupe principal de la classe
        return class_.main_group().students  # type: ignore
    else:
        return []
