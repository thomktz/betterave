from main import db, bcrypt
from app.models.class_ import Class
from app.models.student import Student

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
        class_ = db.session.query(Class).get(class_id)
        if class_:
            new_student.classes.append(class_)

    db.session.commit()

    return new_student.student_id

def get_student_by_id(student_id: int):
    """Get a student by their ID."""
    return db.session.query(Student).get(student_id)

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
def add_class(class_id, name, ects_credits, tutor):
    """Add a class to the database."""
    
    ensae_link = f"https://www.ensae.fr/courses/{class_id}"
    new_class = Class(
        class_id=class_id,
        name=name,
        ects_credits=ects_credits,
        ensae_link=ensae_link,
        tutor=tutor,
    )
    db.session.add(new_class)
    db.session.commit()
    return class_id

def get_all_classes():
    """Return all classes in the database."""
    return Class.query.all()

def get_students_by_class_id(class_id):
    """Get all students enrolled in a class."""
    target_class = db.session.query(Class).get(class_id)
    return target_class.students if target_class else []
