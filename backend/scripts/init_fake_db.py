import random
import datetime
from main import app
from extensions import db
from app.operations.user_operations import add_user, get_user_by_name
from app.operations.class_operations import add_class, authorize_teacher_for_class, get_class_by_id
from app.operations.student_operations import enroll_student_in_class
from app.operations.lesson_operations import add_lesson, assign_students_to_lesson


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

teacher_names = [
    ("Antoine", "Chancel"), 
    ("Laurent", "Linnemer"), 
    ("Olivier", "Loisel"), 
    ("Philippe", "Choné"),
    ("Philippe", "Février"), 
]

assos = [
    ["EJE", "https://www.linkedin.com/company/ensae-junior-etudes/"],
    ["Tribu", "https://www.linkedin.com/company/tribu-ensae/"],
]

def add_weekly_lessons(class_id, start_date, end_date, day_of_week, start_time, end_time, homework=None, room=None, teacher_id=None):
    # Convert day_of_week string to an integer (0=Monday, 6=Sunday)
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    if day_of_week.lower() not in days:
        raise ValueError("Invalid day of the week", day_of_week)

    day_num = days.index(day_of_week.lower())

    # Parse the start_date and end_date strings into datetime.date objects
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    lesson_ids = []
    current_date = start_date
    # Adjust the current_date to the next occurrence of the specified day_of_week
    while current_date.weekday() != day_num and current_date <= end_date:
        current_date += datetime.timedelta(days=1)

    # Now, keep adding lessons for each occurrence of the day_of_week until we reach the end_date
    while current_date <= end_date:
        # Add a new lesson for the current_date
        lesson_id = add_lesson(class_id, current_date, start_time, end_time, homework, room, teacher_id)
        lesson_ids.append(lesson_id)

        # Jump to the next week (next occurrence of the day_of_week)
        current_date += datetime.timedelta(days=7)

    return lesson_ids

classes = [
    {
        "class_id": 1,
        "name": "Introduction à la microéconomie",
        "ects_credits": 3,
        "lesson_times": [
            ("monday", "09:00:00", "10:30:00", "full-class"),
            ("monday", "10:45:00", "12:15:00", "half-class"),
        ],
        "backgroundColor": "#dbb1bc",
        "teachers": random.sample(teacher_names, 2),
    },{
        "class_id": 2,
        "name": "Introduction à la macroéconomie",
        "ects_credits": 3,
        "lesson_times": [
            ("monday", "14:15:00", "15:45:00", "full-class"),
            ("monday", "16:00:00", "17:30:00", "half-class"),
        ],
        "backgroundColor": "#d3c4e3",
        "teachers": random.sample(teacher_names, 2),
    },{
        "class_id": 4,
        "name": "Microéconomie 1 (FR)",
        "ects_credits": 4,
        "lesson_times": [
            ("tuesday", "09:00:00", "10:30:00", "full-class"),
            ("tuesday", "10:45:00", "12:15:00", "half-class"),
        ],
        "backgroundColor": "#8f95d3",
        "teachers": random.sample(teacher_names, 2),
    },{
        "class_id": 5,
        "name": "Macroéconomie 1 (FR)",
        "ects_credits": 4,
        "lesson_times": [
            ("tuesday", "14:15:00", "15:45:00", "full-class"),
            ("tuesday", "16:00:00", "17:30:00", "half-class"),
        ],
        "backgroundColor": "#45b69c",
        "teachers": random.sample(teacher_names, 2),
    },{
        "class_id": 6,
        "name": "Théorie des jeux",
        "ects_credits": 2.5,
        "lesson_times": [
            ("thursday", "09:00:00", "10:30:00", "full-class"),
            ("thursday", "10:45:00", "12:15:00", "half-class"),
        ],
        "backgroundColor": "#D1D0A3",
        "teachers": random.sample(teacher_names, 2),
    },{
        "class_id": 7,
        "name": "Infrastructures et systèmes logiciels",
        "ects_credits": 3,
        "lesson_times": [
            ("thursday", "14:15:00", "15:45:00", "full-class"),
            ("thursday", "16:00:00", "17:30:00", "half-class"),
        ],
        "backgroundColor": "#446BC5",
        "teachers": random.sample(teacher_names, 2),
    },
]

def initialize_database():
    with app.app_context():
        db.create_all()
        
        student_ids = []
        asso_ids = []
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
        
        # 3 - Add teachers
        print("Adding teachers...")
        for (name, surname) in teacher_names:
            teacher_ids.append(
                add_user(
                    name=name,
                    surname=surname,
                    profile_pic=f"photos/{name.lower()}_{surname.lower()}.jpg",
                    user_type="teacher",
                )
            )
        
        # 4 - Add classes
        print("Adding classes...")
        for class_dict in classes:
            class_ids.append(
                add_class(
                    class_id=class_dict["class_id"],
                    name=class_dict["name"],
                    ects_credits=class_dict["ects_credits"],
                    default_teacher_id=get_user_by_name(*class_dict["teachers"][0]).user_id,
                    background_color=class_dict["backgroundColor"],
                )
            )
        
        # 5 - Authorize teachers for classes
        print("Authorizing teachers for classes...")
        for class_dict in classes:
            for teacher in class_dict["teachers"]:
                authorize_teacher_for_class(get_user_by_name(*teacher).user_id, class_dict["class_id"])
                
        # 6 - Enroll students in classes
        print("Enrolling students in classes...")
        for student_id in student_ids:
            for class_id in class_ids:
                if random.random() < 0.7:
                    enroll_student_in_class(student_id, class_id)
        
        # 7 & 8 - Add lessons AND assign students to lessons
        print("Adding lessons and assigning students to lessons...")
        for class_dict in classes:
            class_ = get_class_by_id(class_dict["class_id"])
            enrolled_students = class_.students
            counter = -1
            for (day_of_week, start_time, end_time, lesson_type) in class_dict["lesson_times"]:
                counter += 1
                teacher_id = get_user_by_name(*class_dict["teachers"][counter % len(class_dict["teachers"])]).user_id
                
                if lesson_type == "full-class":
                    room = "A250"
                    students = enrolled_students
                    lesson_ids = add_weekly_lessons(
                        class_id=class_dict["class_id"],
                        start_date="2023-09-01",
                        end_date="2024-01-01",
                        day_of_week=day_of_week,
                        start_time=start_time,
                        end_time=end_time,
                        room=room,
                        teacher_id=teacher_id,
                    )
                    for lesson_id in lesson_ids:
                        assign_students_to_lesson(lesson_id, students)
                else:
                    room_A = str(2000 + random.randint(1, 48))
                    students_A = random.sample(enrolled_students, len(enrolled_students)//2)
                    
                    lesson_ids_A = add_weekly_lessons(
                        class_id=class_dict["class_id"],
                        start_date="2023-09-01",
                        end_date="2024-01-01",
                        day_of_week=day_of_week,
                        start_time=start_time,
                        end_time=end_time,
                        room=room_A,
                        teacher_id=teacher_id,
                    )
                    for lesson_id in lesson_ids_A:
                        assign_students_to_lesson(lesson_id, students_A)
                    
                    counter += 1 # Increment counter to get the next teacher
                    
                    room_B = str(int(room_A) + 1)
                    students_B = [student for student in enrolled_students if student not in students_A]
                    
                    lesson_ids_B = add_weekly_lessons(
                        class_id=class_dict["class_id"],
                        start_date="2023-09-01",
                        end_date="2024-01-01",
                        day_of_week=day_of_week,
                        start_time=start_time,
                        end_time=end_time,
                        room=room_B,
                        teacher_id=get_user_by_name(*class_dict["teachers"][counter % len(class_dict["teachers"])]).user_id,
                    )
                    for lesson_id in lesson_ids_B:
                        assign_students_to_lesson(lesson_id, students_B)
                    
                

if __name__ == "__main__":
    initialize_database()
