from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from app.models import Lesson
from app.operations.user_operations import get_user_by_id

def add_lesson(class_id, date, start_time, end_time, homework=None, room=None, teacher_id=None):
    """Add a lesson to the database."""
    try:
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M:%S").time()
        
        new_lesson = Lesson(
            class_id=class_id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            homework=homework,
            room=room,
            teacher_id=teacher_id
        )
        db.session.add(new_lesson)
        db.session.commit()
        return new_lesson.lesson_id
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding lesson: {str(e)}")
        return -1

def modify_lesson(lesson_id, new_data: dict) -> bool:
    """Modify lesson information in the database."""
    try:
        lesson = get_lesson_by_id(lesson_id)
        if lesson:
            for key, value in new_data.items():
                if hasattr(lesson, key):
                    setattr(lesson, key, value)
            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error modifying lesson: {str(e)}")
        return False

def remove_lesson(lesson_id: int) -> bool:
    """Remove a lesson from the database."""
    try:
        lesson = get_lesson_by_id(lesson_id)
        if lesson:
            db.session.delete(lesson)
            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error deleting lesson: {str(e)}")
        return False
    
def get_lesson_by_id(lesson_id: int) -> Lesson:
    """Get a lesson by its ID."""
    return db.session.get(Lesson, lesson_id)

def get_all_lessons() -> list[Lesson]:
    """Return all lessons in the database."""
    return Lesson.query.all()

def get_lessons_by_class_id(class_id: int) -> list[Lesson]:
    """Get all lessons for a particular class."""
    return Lesson.query.filter_by(class_id=class_id).all()

def get_lessons_by_student_id(user_id: int) -> list[Lesson]:
    """Get all lessons a particular student is part of."""
    # This requires the ORM to have a reverse relationship set up.
    student = get_user_by_id(user_id)
    return student.lessons

def assign_students_to_lesson(lesson_id, students: list):
    """Assign a list of students to a lesson."""
    try:
        lesson = get_lesson_by_id(lesson_id)
        if lesson:
            lesson.students.extend(students)
            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error assigning students to lesson: {str(e)}")
        return False

def add_student_to_lesson(lesson_id, student):
    """Assign a single student to a lesson."""
    try:
        lesson = get_lesson_by_id(lesson_id)
        if lesson:
            lesson.students.append(student)
            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding student to lesson: {str(e)}")
        return False