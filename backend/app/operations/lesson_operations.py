# type: ignore
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from backend.extensions import db
from backend.app.decorators import with_instance
from backend.app.models import Lesson, ClassGroup, Class, User


def add_lesson(
    group_id: int,
    date: str,
    start_time: str,
    end_time: str,
    homework: str = None,
    room: str = None,
    teacher_id: int = None,
):
    """Add a lesson to the database."""
    try:
        # Validate and convert date and time if provided as strings
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M").time()
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M").time()

    except ValueError as e:
        print(f"Error in date or time conversion: {str(e)}")
        return -1

    try:
        new_lesson = Lesson(
            group_id=group_id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            homework=homework,
            room=room,
            teacher_id=teacher_id,
        )
        db.session.add(new_lesson)
        db.session.commit()
        return new_lesson.lesson_id
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding lesson: {str(e)}")
        return -1


@with_instance(Lesson)
def update_lesson(lesson: Lesson, new_data: dict) -> bool:
    """Modify lesson information in the database."""
    try:
        for key, value in new_data.items():
            if hasattr(lesson, key):
                setattr(lesson, key, value)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error modifying lesson: {str(e)}")
        return False


@with_instance(Lesson)
def delete_lesson(lesson: Lesson) -> bool:
    """Remove a lesson from the database."""
    try:
        db.session.delete(lesson)
        db.session.commit()
        return True
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


def get_all_future_lessons(sort: bool = True) -> list[Lesson]:
    """Return all lessons in the database."""
    if sort:
        return sorted(Lesson.query.filter(Lesson.date >= datetime.now().date()).all())
    return Lesson.query.filter(Lesson.date >= datetime.now().date()).all()


@with_instance(Class)
def get_lessons_by_class(class_: Class) -> list[Lesson]:
    """Get all lessons for a particular class."""
    return Lesson.query.join(ClassGroup).filter(ClassGroup.class_id == class_.class_id).all()


@with_instance(User)
def get_student_lessons(user: User, limit: int = None, sort: bool = True) -> list[Lesson]:
    """Get all lessons associated with a student through class groups."""
    # Collect lessons from all groups where the student is enrolled
    lessons = []
    for group in user.groups:
        all_lessons = group.lessons
        lessons.extend(all_lessons)

    if limit is not None:
        return sorted(lessons)[:limit] if sort else lessons[:limit]
    else:
        return sorted(lessons) if sort else lessons


@with_instance(User)
def get_student_future_lessons(user: User, limit: int = None, sort: bool = True) -> list[Lesson]:
    """Get future lessons for a student through class groups."""
    # Retrieve all lessons for the student from their groups
    future_lessons = []
    date = datetime.now().date()
    for group in user.groups:
        all_lesson = group.lessons
        group_lessons = [lesson for lesson in all_lesson if lesson.date >= date]
        future_lessons.extend(group_lessons)

    if limit is not None:
        return sorted(future_lessons)[:limit] if sort else future_lessons[:limit]
    else:
        return sorted(future_lessons) if sort else future_lessons


@with_instance(User)
def get_teacher_lessons(teacher: User, limit: int = None, sort: bool = True) -> list[Lesson]:
    """Get all lessons associated with a teacher."""
    # The lessons_taught relationship gives us direct access to the lessons

    lessons = teacher.lessons_taught.limit(limit) if limit is not None else teacher.lessons_taught
    lessons = lessons.all()

    return sorted(lessons) if sort else lessons


@with_instance(User)
def get_teacher_future_lessons(teacher: User, limit: int = None, sort: bool = True) -> list[Lesson]:
    """Get future lessons for a teacher."""
    # Using the lessons_taught relationship to filter future lessons
    future_lessons = (
        teacher.lessons_taught.filter(Lesson.date >= datetime.now().date()).limit(limit).all()
        if limit is not None
        else teacher.lessons_taught.filter(Lesson.date >= datetime.now().date()).all()
    )

    return sorted(future_lessons) if sort else future_lessons
