from datetime import datetime
from extensions import db
from app.models import Grade, Class
from app.decorators import with_instance
from app.operations.class_operations import get_class_by_id


def get_grades_by_class_id(class_id: int):
    """Retrieve grades for a specific class."""
    return sorted(Grade.query.filter_by(class_id=class_id).all())

def get_grades_by_student(student_id: int):
    """Retrieve grades for a specific class."""
    return sorted(Grade.query.filter_by(student_id=student_id).all())

@with_instance(Grade)
def delete_grade(grade: Grade):
    """Delete a grade."""
    if grade:
        db.session.delete(grade)
        db.session.commit()
        return True
    return False

def add_grade_to_student(student_id, class_id, grade_value):
    """Add a grade to a specific student in a class."""
    class_ = get_class_by_id(class_id)
    if class_ and class_.main_group():
        # Check if the student is part of the class
        student_in_class = any(student.student_id == student_id for student in class_.students)
        
        if not student_in_class:
            # If the student is not in the class, add them to the main group
            add_student_to_group(student_id, class_.main_group().group_id)

        # Add grade to the main group of the class.
        return add_grade_to_group(student_id, grade_value, class_.main_group().group_id)
    else:
        # Handle the case where the class or main group doesn't exist.
        return None