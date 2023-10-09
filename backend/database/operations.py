from database.session import SessionLocal as Session
from models.student import Student
from models.class_ import Class, student_classes

def add_student(name, surname, profile_pic, level, enrolled_classes_ids):
    with Session() as session:
        new_student = Student(name=name, surname=surname, profile_pic=profile_pic, level=level)
        for class_id in enrolled_classes_ids:
            assoc = student_classes.insert().values(student_id=new_student.student_id, class_id=class_id)
            session.execute(assoc)
        session.add(new_student)
        session.commit()

def add_class(class_id, name, ects_credits, tutor):
    ensae_link = f"https://www.ensae.fr/courses/{class_id}"
    with Session() as session:
        new_class = Class(class_id=class_id, name=name, ects_credits=ects_credits, ensae_link=ensae_link, tutor=tutor)
        session.add(new_class)
        session.commit()

def get_all_classes():
    with Session() as session:
        return session.query(Class).all()

def get_all_students():
    with Session() as session:
        return session.query(Student).all()

def get_students_by_class_id(class_id):
    with Session() as session:
        target_class = session.query(Class).filter_by(class_id=class_id).first()
        return target_class.students if target_class else []

# If needed, you can also add more operations such as update and delete.
