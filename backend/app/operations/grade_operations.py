from datetime import datetime
from extensions import db
from app.models import Grade, Class
from app.decorators import with_instance
from app.operations.class_operations import get_class_by_id

def add_grade(student_id, class_id, grade_value):
    """Add a grade for a student in a class."""
    grade = Grade(student_id=student_id, class_id=class_id, grade=grade_value)

    try:
        # Add the grade to the database
        db.session.add(grade)
        db.session.commit()
        return grade
    except Exception as e:
        # Handle any exceptions, e.g., log the error
        print(f"Error adding grade: {e}")
        db.session.rollback()
        return None
    
def get_grades_by_student_and_class_id(student_id: int, class_id: int):
    """Retrieve grades for a specific student in a specific class."""
    return sorted(Grade.query.filter_by(student_id=student_id, class_id=class_id).all())

# def get_grades_by_class_id(class_id: int):
#     """Retrieve grades for a specific class."""
#     return sorted(Grade.query.filter_by(class_id=class_id).all())

# def get_grades_by_student(student_id: int):
#     """Retrieve grades for a specific class."""
#     return sorted(Grade.query.filter_by(student_id=student_id).all())

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
    
def update_student_grade(class_id, student_id, new_grade):
    """Update the grade for a specific student in a specific class."""
    try:
        # Utilisez la fonction d'accès aux données appropriée pour mettre à jour la note
        db_update_student_grade(class_id, student_id, new_grade)
        return True
    except Exception as e:
        # Gérez l'erreur (log, notification, etc.)
        print(f"Error updating student grade: {e}")
        return False
    
def update_student_grade(class_id, student_id, new_grade):
    """Update the grade for a specific student in a specific class."""
    try:
        # Récupérer l'objet Grade à partir de la base de données
        grade = Grade.query.filter_by(class_id=class_id, student_id=student_id).first()

        if grade:
            # Mettre à jour la note
            grade.grade = new_grade

            # Enregistrez les modifications dans la base de données
            db.session.commit()

            return True
        else:
            # Gérer le cas où l'entrée de grade n'existe pas
            print("Grade entry not found.")
            return False
    except Exception as e:
        # Gérez l'erreur (log, notification, etc.)
        print(f"Error updating student grade: {e}")
        db.session.rollback()
        return False