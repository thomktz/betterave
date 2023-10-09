import bcrypt
from app.database.session import SessionLocal as Session
from app.models.student import Student
from app.models.class_ import Class, student_classes


### Student operations ###

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(hashed_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def add_student(name, surname, profile_pic, level, enrolled_classes_ids):
    # Generate email
    email = f"{name.lower()}.{surname.replace(' ', '-').lower()}@ensae.fr"
    
    # Generate the default password and hash it
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
            level=level
        )        
        for class_id in enrolled_classes_ids:
            assoc = student_classes.insert().values(student_id=new_student.student_id, class_id=class_id)
            session.execute(assoc)
        session.add(new_student)
        session.commit()
        
        # Get the student ID after the session is commited
        student_id = new_student.student_id
        print("STUDENT ID", new_student.student_id)
        
    return student_id

def get_student_by_id(student_id: int):
    with Session() as session:
        return session.query(Student).filter_by(student_id=student_id).first()

def get_student_by_email(email: str):
    with Session() as session:
        return session.query(Student).filter_by(email=email).first()

def authenticate_student(email: str, password: str) -> bool:
    student = get_student_by_email(email)
    if not student:
        return False
    return check_password(student.hashed_password, password)

def get_all_students():
    with Session() as session:
        return session.query(Student).all()


### Class operations ###

def add_class(class_id, name, ects_credits, tutor):
    ensae_link = f"https://www.ensae.fr/courses/{class_id}"
    with Session() as session:
        new_class = Class(class_id=class_id, name=name, ects_credits=ects_credits, ensae_link=ensae_link, tutor=tutor)
        session.add(new_class)
        session.commit()
    return class_id

def get_all_classes():
    with Session() as session:
        return session.query(Class).all()

def get_students_by_class_id(class_id):
    with Session() as session:
        target_class = session.query(Class).filter_by(class_id=class_id).first()
        return target_class.students if target_class else []