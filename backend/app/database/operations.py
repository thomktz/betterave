from datetime import datetime
from extensions import db, bcrypt
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.class_ import Class

### Student operations ###
def hash_password(password: str) -> str:
    """Hash a given password."""
    return bcrypt.generate_password_hash(password).decode("utf-8")

def check_password(hashed_password, password):
    """Check if a given password matches a hashed password."""
    return bcrypt.check_password_hash(hashed_password, password)
   
def add_student(name: str, surname: str, profile_pic: str, level: str, enrolled_classes_ids: list):
    """Add a student to the database."""
    
    email = f"{name.lower()}.{surname.replace(' ', '-').lower()}@ensae.fr"
    password = f"{name[0].lower()}{surname.replace(' ', '-').lower()}"
    hashed_password = hash_password(password)

    new_student = Student(
        email=email,
        hashed_password=hashed_password,
        name=name,
        surname=surname,
        profile_pic=profile_pic,
        level=level,
    )
    
    # Add the student to the session first
    db.session.add(new_student)

    # Associating the student with classes
    for class_id in enrolled_classes_ids:
        class_ = db.session.get(Class, class_id)
        if class_:
            new_student.classes.append(class_)

    db.session.commit()

    return new_student.student_id

def get_student_by_id(student_id: int):
    """Get a student by their ID."""
    return db.session.get(Student, student_id)

def get_student_by_email(email: str):
    """Get a student by their email."""
    return Student.query.filter_by(email=email).first()

def authenticate_student(email: str, password: str) -> bool:
    """Authenticate a student using their email and password."""
    student = get_student_by_email(email)
    if not student:
        return False
    return check_password(student.hashed_password, password)

def get_all_students():
    """Return all students in the database."""
    return Student.query.all()

### Class operations ###
def add_class(class_id, name, ects_credits, tutor, backgroundColor, **kwargs):
    """Add a class to the database."""
    
    ensae_link = f"https://www.ensae.fr/courses/{class_id}"
    new_class = Class(
        class_id=class_id,
        name=name,
        ects_credits=ects_credits,
        ensae_link=ensae_link,
        tutor=tutor,
        backgroundColor=backgroundColor,
    )
    db.session.add(new_class)
    db.session.commit()
    return class_id

def get_all_classes():
    """Return all classes in the database."""
    return Class.query.all()

def get_students_by_class_id(class_id):
    """Get all students enrolled in a class."""
    target_class = db.session.get(Class, class_id)
    return target_class.students if target_class else []

### Lesson operations ###

def add_lesson(class_id, date, start_time, end_time, homework=None, room=None, tutor=None):
    """Add a lesson to the database."""
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
        tutor=tutor
    )
    db.session.add(new_lesson)
    db.session.commit()
    return new_lesson.lesson_id

def get_lesson_by_id(lesson_id: int):
    """Get a lesson by its ID."""
    return db.session.get(Lesson, lesson_id)

def get_all_lessons():
    """Return all lessons in the database."""
    return Lesson.query.all()

def get_lessons_by_class_id(class_id: int):
    """Get all lessons for a particular class."""
    return Lesson.query.filter_by(class_id=class_id).all()

def update_lesson(lesson_id: int, **kwargs):
    """Update attributes of a lesson."""
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        return None
    
    for key, value in kwargs.items():
        if hasattr(lesson, key):
            setattr(lesson, key, value)
    
    db.session.commit()
    return lesson_id

def delete_lesson(lesson_id: int):
    """Delete a lesson by its ID."""
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        return False
    
    db.session.delete(lesson)
    db.session.commit()
    return True

def get_lessons_by_student(student_id: int):
    """Get all lessons for a particular student."""
    
    # Fetch the student from the database
    student = get_student_by_id(student_id)
    if not student:
        return []

    # Fetch all the classes the student is enrolled in
    enrolled_classes = student.classes

    # For each class, get the associated lessons
    lessons = []
    for class_ in enrolled_classes:
        lessons.extend(get_lessons_by_class_id(class_.class_id))

    return sorted(lessons)
