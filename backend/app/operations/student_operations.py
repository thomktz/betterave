from extensions import db
from app.models import User, Class
from app.models.user import UserType

def enroll_student_in_class(user_id: int, class_id: int):
    """Enroll a student in a class."""
    student = db.session.get(User, user_id)
    if not student:
        return False
    
    class_instance = db.session.get(Class, class_id)
    if not class_instance:
        return False

    student.enrolled_classes.append(class_instance)
    db.session.commit()
    return True

def remove_student_from_class(user_id: int, class_id: int):
    """Remove a student from a class."""
    student = db.session.get(User, user_id)
    if not student:
        return False
    
    class_instance = db.session.get(Class, class_id)
    if not class_instance:
        return False

    student.enrolled_classes.remove(class_instance)
    db.session.commit()
    return True

def get_student_classes(user_id: int):
    """Get all classes a student is enrolled in."""
    student = db.session.get(User, user_id)
    if not student:
        return []

    return student.enrolled_classes

def get_student_lessons(user_id: int):
    """Get all lessons associated with a student."""
    student = db.session.get(User, user_id)
    if not student:
        return []

    return student.lessons

def get_student_future_lessons(user_id: int, current_time):
    """Get future lessons for a student."""
    student = db.session.get(User, user_id)
    if not student:
        return []

    # Retrieve all lessons for the student
    all_lessons = student.lessons

    # Filter lessons to get only future lessons
    future_lessons = [lesson for lesson in all_lessons if lesson.date >= current_time.date()]

    return future_lessons

def get_student_lessons(user_id: int):
    """Get lessons that a student is registered to."""
    student = db.session.get(User, user_id)
    if not student:
        return []

    return sorted(student.registered_lessons)

def get_all_students():
    """Return all student users in the database."""
    return User.query.filter_by(user_type=UserType("student")).all()

def is_student_in_class(student: User, class_id: int):
    """Check if a student is in a specific class."""
    class_instance = Class.query.get(class_id)
    if not class_instance:
        return False
    return student in class_instance.students