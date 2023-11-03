import random
import datetime
import json
from main import app
from extensions import db
from app.operations.user_operations import add_user, get_user_by_name
from app.operations.class_operations import add_class, authorize_teacher_for_class, get_class_by_id
from app.operations.student_operations import enroll_student_in_class
from app.operations.lesson_operations import add_lesson, assign_students_to_lesson


with open('data/classes.json', 'r') as fichier_json:
    classes = json.load(fichier_json)


student_names = [
    ("Alice", "Adams"), 
    ("Bob", "Baker"), 
    ("Carol", "Clark"), 
    ("Dave", "Davis"), 
    ("Eve", "Evans"), 
    ("Fred", "Frank"), 
    ("Grace", "Ghosh"), 
    ("Hal", "Hills"), 
    ("Isaac", "Irwin"), 
    ("Julia", "Jones"), 
    ("Karl", "Klein"), 
    ("Lara", "Lopez"), 
    ("Max", "Mason"), 
    ("Nora", "Nalty"), 
    ("Oscar", "Ochoa"), 
    ("Paul", "Patel"), 
    ("Quinn", "Quinn"), 
    ("Rob", "Reily"), 
    ("Susan", "Smith"), 
    ("Tom", "Trott"), 
    ("Ursula", "Usman"), 
    ("Victor", "Valdo"), 
    ("Wendy", "White"), 
    ("Xavier", "Xiang"), 
    ("Yara", "Yakub"), 
    ("Zack", "Zafar"), 
    ("Claire", "Dechaux"), 
    ("Thomas", "Kientz"), 
    ("Clothilde", "Voisin"), 
]

assos = [
    ["EJE", "https://www.linkedin.com/company/ensae-junior-etudes/"],
    ["Tribu", "https://www.linkedin.com/company/tribu-ensae/"],
]

admins = [
    ("admin", "admin"),
]

def initialize_database():
    with app.app_context():
        db.create_all()
        
        student_ids = []
        asso_ids = []
        admin_ids = []
        teacher_ids = []
        class_ids = []
        lesson_ids = []
        
        # 1 - Add students
        print("Adding students...")
        for (name, surname) in student_names:
            student_ids.append(
                add_user(
                    name=name,
                    surname=surname,
                    profile_pic=f"photos/{name.lower()}_{surname.lower()}.jpg",
                    user_type="student",
                    level=str(random.randint(1, 3))+"A",
                )
            )
        
        # 2 - Add associations
        print("Adding associations...")
        for asso in assos:
            asso_ids.append(
                add_user(
                    name=asso[0],
                    surname="",
                    profile_pic=f"photos/{asso[0].lower()}.jpg",
                    user_type="asso",
                    email_override=f"{asso[0].lower()}@ensae.fr",
                    linkedin=asso[1],
                )
            )
        
        # 3 - Add admins
        print("Adding admins...")
        for admin_name, password in admins:
            admin_ids.append(
                add_user(
                    name=admin_name,
                    surname="",
                    profile_pic=f"photos/{admin_name.lower()}.jpg",
                    user_type="admin",
                    email_override=f"{admin_name.lower()}@ensae.fr",
                    password_override=password,
                )
            )
            
        
        # 4 - Add teachers
        print("Adding teachers...")
        teacher_set = set()
        for class_dict in classes:
            teacher_name = tuple(class_dict["teacher_name"])
            if teacher_name not in teacher_set: # Prevent from creating a new user for a teacher already seen
                teacher_set.add(teacher_name)
                name, surname = teacher_name
                teacher_ids.append(
                    add_user(
                        name=name,
                        surname=surname,
                        profile_pic=f"photos/{name.lower()}_{surname.lower()}.jpg",
                        user_type="teacher",
                    )
                )
            for (date, start_time, end_time, lesson_type, teacher, room) in class_dict["lesson_info"]:
                teacher_name = tuple(teacher)
                if teacher_name not in teacher_set: # Prevent from creating a new user for a teacher already seen
                    teacher_set.add(teacher_name)
                    name, surname = teacher_name
                    teacher_ids.append(
                        add_user(
                            name=name,
                            surname=surname,
                            profile_pic=f"photos/{name.lower()}_{surname.lower()}.jpg",
                            user_type="teacher",
                        )
                    )
        
        # 5 - Add classes
        print("Adding classes...")
        for class_dict in classes:
            class_ids.append(
                add_class(
                    class_id=class_dict["class_id"],
                    name=class_dict["name"],
                    ects_credits=class_dict["ects"],
                    default_teacher_id=get_user_by_name(*class_dict["teacher_name"]).user_id,
                    backgroundColor=class_dict["backgroundColor"],
                )
            )
        
        # 6 - Authorize teachers for classes
        print("Authorizing teachers for classes...")
        for class_dict in classes:
            authorize_teacher_for_class(get_user_by_name(*class_dict["teacher_name"]).user_id, class_dict["class_id"])
            for (date, start_time, end_time, lesson_type, teacher, room) in class_dict["lesson_info"]:
                authorize_teacher_for_class(get_user_by_name(*teacher).user_id, class_dict["class_id"])
                
        # 7 - Enroll students in classes
        print("Enrolling students in classes...")
        for student_id in student_ids:
            for class_id in class_ids:
                if random.random() < 0.1:
                    enroll_student_in_class(student_id, class_id)
        
        # 8 & 9 - Add lessons AND assign students to lessons
        print("Adding lessons and assigning students to lessons...")
        for class_dict in classes:
            class_id = class_dict["class_id"]
            class_ = get_class_by_id(class_id)
            enrolled_students = class_.students
            for (date, start_time, end_time, lesson_type, teacher, room) in class_dict["lesson_info"]:
                teacher_id = get_user_by_name(*teacher).user_id

                homework=None
                students = enrolled_students

                lesson_id = add_lesson(class_id, date, start_time, end_time, homework, room, teacher_id)
                assign_students_to_lesson(lesson_id, students)
                lesson_ids.append(lesson_id)
                

if __name__ == "__main__":
    initialize_database()
