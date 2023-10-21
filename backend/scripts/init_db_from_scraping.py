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



teacher_names = []

for class_dict in classes:
    if class_dict["teacher_name"]=="TBD":
        class_dict["teacher_name"]=['FÉVRIER', 'Philippe']
    if class_dict["teacher_name"]==['ZERBIB', 'Olivier', 'David']:
        class_dict["teacher_name"]=['ZERBIB', 'Olivier']


for class_dict in classes:
    if class_dict["teacher_name"] not in teacher_names:
        teacher_names.append(class_dict["teacher_name"])
# print(teacher_names)



# teacher_names = [
#     ("Antoine", "Chancel"), 
#     ("Laurent", "Linnemer"), 
#     ("Olivier", "Loisel"), 
#     ("Philippe", "Choné"),
#     ("Philippe", "Février"), 
# ]


def initialize_database():
    with app.app_context():
        db.create_all()
        
        student_ids = []
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
        
        # 2 - Add teachers
        print("Adding teachers...")
        # print(teacher_names)
        for complete_name in teacher_names:
            name = complete_name[0]
            surname = complete_name[1]
            teacher_ids.append(
                add_user(
                    name=name,
                    surname=surname,
                    profile_pic=f"photos/{name.lower()}_{surname.lower()}.jpg",
                    user_type="teacher",
                )
            )
        
        # 3 - Add classes
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
        
        # 4 - Authorize teachers for classes
        print("Authorizing teachers for classes...")
        for class_dict in classes:
            # for teacher in class_dict["teacher_name"]:
            #     print(teacher)
            # authorize_teacher_for_class(get_user_by_name(*teacher).user_id, class_dict["class_id"])
            authorize_teacher_for_class(get_user_by_name(*class_dict["teacher_name"]).user_id, class_dict["class_id"])
                
        # 5 - Enroll students in classes
        print("Enrolling students in classes...")
        for student_id in student_ids:
            for class_id in class_ids:
                if random.random() < 0.7:
                    enroll_student_in_class(student_id, class_id)
        
        # 6 & 7 - Add lessons AND assign students to lessons
        print("Adding lessons and assigning students to lessons...")
        for class_dict in classes:
            class_id = class_dict["class_id"]
            class_ = get_class_by_id(class_id)
            enrolled_students = class_.students
            counter = -1
            for (date, start_time, end_time, lesson_type, teacher, room) in class_dict["lesson_info"]:
                counter += 1
                # teacher_id = get_user_by_name(*class_dict["teachers"][counter % len(class_dict["teachers"])]).user_id
                teacher_id = get_user_by_name(*class_dict["teacher_name"]).user_id

                homework=None
                students = enrolled_students

                lesson_id = add_lesson(class_id, date, start_time, end_time, homework, room, teacher_id)
                lesson_ids.append(lesson_id)

            for lesson_id in lesson_ids:
                assign_students_to_lesson(lesson_id, students)
                    
                

if __name__ == "__main__":
    initialize_database()
