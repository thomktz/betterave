import bcrypt

from app.database.session import SessionLocal as Session
from app.models.class_ import Class, student_classes
from app.models.student import Student

### Student operations ###
def hash_password(password: str) -> str:
    """Hash a given password

    Args:
        password (str): The password to hash

    Returns:
        str: Hashed password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(hashed_password: str, password: str) -> bool:
    """Check if a given password matches a hashed password

    Args:
        hashed_password (str): Hashed password
        password (str): Password to check

    Returns:
        bool: Whether the password matches the hashed password
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def add_student(name: str, surname: str, profile_pic: str, level: str, enrolled_classes_ids: list):
    """Add a student to the database

    Args:
        name (str): Name of the student
        surname (str): Surame of the student
        profile_pic (str): Link to the student's profile picture
        level (str): Level of the student (e.g., 1A, 2A, ...)
        enrolled_classes_ids (list): List of class IDs the student is enrolled in

    Returns:
        str: Student ID
    """
    # Generate email in the ENSAE format
    email = f"{name.lower()}.{surname.replace(' ', '-').lower()}@ensae.fr"
    # Default password is the first letter of the name + the surname
    password = f"{name[0].lower()}{surname.replace(' ', '-').lower()}"

    hashed_password = hash_password(password)
    student_id = None
    with Session() as session:
        new_student = Student(
            email=email,
            hashed_password=hashed_password,
            name=name,
            surname=surname,
            profile_pic=profile_pic,
            level=level,
        )
        for class_id in enrolled_classes_ids:
            assoc = student_classes.insert().values(student_id=new_student.student_id, class_id=class_id)
            session.execute(assoc)
        session.add(new_student)
        session.commit()

        # Get the student ID after the session is commited
        student_id = new_student.student_id

    return student_id


def get_student_by_id(student_id: int):
    """Get a student by their ID"""
    with Session() as session:
        return session.query(Student).filter_by(student_id=student_id).first()


def get_student_by_email(email: str):
    """Get a student by their email"""
    with Session() as session:
        return session.query(Student).filter_by(email=email).first()


def authenticate_student(email: str, password: str) -> bool:
    """Authenticate a student using their email and password"""
    student = get_student_by_email(email)
    if not student:
        return False
    return check_password(student.hashed_password, password)


def get_all_students():
    """Return all students in the database"""
    with Session() as session:
        return session.query(Student).all()


### Class operations ###
def add_class(class_id, name, ects_credits, tutor):
    """Add a class to the database

    Args:
        class_id (str): Class ID
        name (str): Name of the class
        ects_credits (float): ECTS credits of the class
        tutor (str): Tutor of the class

    Returns:
        str: Class ID
    """
    ensae_link = f"https://www.ensae.fr/courses/{class_id}"
    with Session() as session:
        new_class = Class(
            class_id=class_id,
            name=name,
            ects_credits=ects_credits,
            ensae_link=ensae_link,
            tutor=tutor,
        )
        session.add(new_class)
        session.commit()
    return class_id


def get_all_classes():
    """Return all classes in the database"""
    with Session() as session:
        return session.query(Class).all()


def get_students_by_class_id(class_id):
    """Get all students enrolled in a class"""
    with Session() as session:
        target_class = session.query(Class).filter_by(class_id=class_id).first()
        return target_class.students if target_class else []
