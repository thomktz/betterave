from typing import Optional
from backend.extensions import db
from backend.app.models import Grade


def add_grade(student_id: int, class_id: int, grade_value: float) -> Optional[Grade]:
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


def get_grades_by_student_and_class_id(student_id: int, class_id: int) -> list[Grade]:
    """Retrieve grades for a specific student in a specific class."""
    return sorted(Grade.query.filter_by(student_id=student_id, class_id=class_id).all())


def update_student_grade(class_id: int, student_id: int, new_grade: float) -> bool:
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
            add_grade(student_id, class_id, new_grade)
            # Gérer le cas où l'entrée de grade n'existe pas
            return True
    except Exception as e:
        # Gérez l'erreur (log, notification, etc.)
        print(f"Error updating student grade: {e}")
        db.session.rollback()
        return False
