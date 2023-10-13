from datetime import datetime
from extensions import db, bcrypt
from app.models.user import User
from app.models.lesson import Lesson
from app.models.class_ import Class

### User operations ###
def hash_password(password: str) -> str:
    """Hash a given password."""
    return bcrypt.generate_password_hash(password).decode("utf-8")

def check_password(hashed_password, password):
    """Check if a given password matches a hashed password."""
    return bcrypt.check_password_hash(hashed_password, password)
   
def add_user(name: str, surname: str, profile_pic: str, level: str,user_type : str, enrolled_classes_ids: list):
    """Add a user to the database."""
    
    email = f"{name.lower()}.{surname.replace(' ', '-').lower()}@ensae.fr"
    password = f"{name[0].lower()}{surname.replace(' ', '-').lower()}"
    hashed_password = hash_password(password)

    new_user = User(
        email=email,
        hashed_password=hashed_password,
        name=name,
        surname=surname,
        profile_pic=profile_pic,
        level=level,
        user_type=user_type
    )
    
    # Add the user to the session first
    db.session.add(new_user)
    if user_type=='student':
        # Associating the user with classes
        for class_id in enrolled_classes_ids:
            class_ = db.session.get(Class, class_id)
            if class_:
                new_user.classes.append(class_)

    if user_type=="teacher":
        teacher_classes = Class.query.filter_by(tutor=f"{new_user.surname} {new_user.name}").all()
        new_user.classes.extend(teacher_classes)

    db.session.commit()

    return new_user.user_id

def get_user_by_id(user_id: int):
    """Get a user by their ID."""
    return db.session.get(User, user_id)

def get_user_by_email(email: str):
    """Get a user by their email."""
    return User.query.filter_by(email=email).first()

def get_user_by_name(name: str):
    """Get a user by their name."""
    return User.query.filter_by(name=name).first()

def get_user_by_surname(surname: str):
    """Get a user by their name."""
    return User.query.filter_by(surname=surname).first()

def authenticate_user(email: str, password: str) -> bool:
    """Authenticate a user using their email and password."""
    user = get_user_by_email(email)
    if not user:
        return False
    return check_password(user.hashed_password, password)

def get_all_users():
    """Return all users in the database."""
    return User.query.all()

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

def get_users_by_class_id(class_id):
    """Get all users enrolled in a class."""
    target_class = db.session.get(Class, class_id)
    return target_class.users if target_class else []

def get_class_by_tutor(name_tutor : str) -> list:
    """Get all classes given by a tutor."""
    return Class.query.filter_by(tutor=name_tutor).all()


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

def get_lessons_by_user(user_id: int):
    """Get all lessons for a particular user."""
    
    # Fetch the user from the database
    user = get_user_by_id(user_id)
    if not user:
        return []

    # Fetch all the classes the user is enrolled in
    enrolled_classes = user.classes

    # For each class, get the associated lessons
    lessons = []
    for class_ in enrolled_classes:
        lessons.extend(get_lessons_by_class_id(class_.class_id))

    return sorted(lessons)
