from extensions import db
from app.decorators import with_instance
from app.models import User, ClassGroup, Class, Lesson
from app.models.user import UserType, UserLevel
from sqlalchemy import func

@with_instance(User)
def get_student_groups(user: User):
    """Get all class groups a student is enrolled in."""
    return user.enrolled_groups

@with_instance(User)
def get_student_lessons(user: User, sort: bool = True) -> list[Lesson]:
    """Get all lessons associated with a student through class groups."""
    # Collect lessons from all groups where the student is enrolled
    lessons = []
    for group in user.groups:
        lessons.extend(group.lessons)

    return sorted(lessons) if sort else lessons

@with_instance(User)
def get_student_future_lessons(user: User, current_time, sort: bool = True) -> list[Lesson]:
    """Get future lessons for a student through class groups."""
    # Retrieve all lessons for the student from their groups
    future_lessons = []
    for group in user.groups:
        group_lessons = [lesson for lesson in group.lessons if lesson.date >= current_time.date()]
        future_lessons.extend(group_lessons)

    return sorted(future_lessons) if sort else future_lessons

def get_all_students():
    """Return all student users in the database."""
    # Assuming UserType is an enum and "student" is one of its members
    return User.query.filter(User.user_type == UserType.STUDENT).all()

def get_students_from_level(level: UserLevel):
    """Return all student users from a specific level."""
    return User.query.filter(User.user_type == UserType.STUDENT, User.level == level).all()

@with_instance([User, ClassGroup])
def is_student_in_group(student: User, group: ClassGroup):
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