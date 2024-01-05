"""Initialize the database with dummy data."""

import random
import json
import numpy as np
import pandas as pd
from main import app
from extensions import db
from app.operations.user_operations import add_user, get_user_by_name
from app.operations.student_operations import get_students_from_level
from app.operations.class_operations import add_class, get_classes_from_level, get_class_by_id
from app.operations.lesson_operations import add_lesson
from app.operations.class_group_operations import (
    add_class_group,
    enroll_student_in_group,
    get_class_group_by_name,
)
from app.operations.event_operations import add_event
from app.operations.grade_operations import add_grade
from app.operations.user_class_group_operations import add_user_class_group
from app.operations.asso_operations import subscribe_to_asso
from app.operations.message_operations import add_class_message
from app.operations.homework_operations import add_homework_to_class
from app.models import UserLevel

CLASSES_PER_STUDENT = 10

with open("data/classes.json", "r") as fichier_json:
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

homework_contents = [
    "Do exercices 1 to 10 of chapter 1.",
    "Read chapter 2.",
    "Assigned reading: https://download.arxiv.org/pdf/1706.03762.pdf",
    "Read chapter 3.",
    "Prepare exercices 1 to 10 of chapter 2.",
    "Team project: Build a website",
    "Learn the basics of Python.",
    "Read chapter 4.",
]


def initialize_database() -> None:
    """Initialize the database with dummy data."""
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()

        student_ids = []
        asso_ids = []
        admin_ids = []
        teacher_ids = []
        class_ids = []
        lesson_ids = []

        # 1 - Add students
        print("Adding students...")
        for name, surname in student_names:
            student_ids.append(
                add_user(
                    name=name,
                    surname=surname,
                    profile_pic=f"photos/{name.lower()}_{surname.lower()}.jpg",
                    user_type="student",
                    level=str(random.randint(1, 3)) + "A",
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
            if teacher_name not in teacher_set:
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
            for _, _, _, _, teacher, _ in class_dict["lesson_info"]:
                teacher_name = tuple(teacher)
                if teacher_name not in teacher_set:
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
        print("Adding classes and class groups...")
        for class_dict in classes:
            class_ids.append(
                add_class(
                    class_id=class_dict["class_id"],
                    name=class_dict["name"],
                    ects_credits=class_dict["ects"],
                    default_teacher_id=get_user_by_name(*class_dict["teacher_name"]).user_id,
                    background_color=class_dict["backgroundColor"],
                    level=class_dict["level"],
                )
            )

            # Add main class group
            add_class_group(
                name="Cours",
                class_id=class_dict["class_id"],
                is_main_group=True,
            )

            # 6 - Add secondary class groups
            lesson_types = set(["Cours"])
            for lesson in class_dict["lesson_info"]:
                _, start_time, end_time, lesson_type, teacher, room = lesson
                if lesson_type not in lesson_types:
                    lesson_types.add(lesson_type)
                    add_class_group(
                        name=lesson_type,
                        class_id=class_dict["class_id"],
                        is_main_group=False,
                    )

            # 7 - Add welcome message
            add_class_message(
                content=(
                    f"Welcome to class '{class_dict['name']}'! "
                    + "Here, you can ask questions to your teacher and other enrolled students."
                ),
                class_id=class_dict["class_id"],
                user_id=admin_ids[0],
            )

        # 8 - Enroll students in groups
        for level in UserLevel:
            students = get_students_from_level(level)
            level_classes = get_classes_from_level(level)
            for student in students:
                picked_classes = np.random.choice(level_classes, size=CLASSES_PER_STUDENT, replace=False)
                for class_ in picked_classes:
                    primary_group = class_.main_group()
                    secondary_group = None

                    # Enroll the student in the groups
                    enroll_student_in_group(student.user_id, primary_group.group_id)

                    # Check for secondary groups and select one if they exist
                    secondary_groups = class_.secondary_groups()
                    if secondary_groups:
                        secondary_group = np.random.choice(secondary_groups)
                        enroll_student_in_group(student.user_id, secondary_group.group_id)

                    # Create a UserClassGroup entry
                    add_user_class_group(
                        user_id=student.user_id,
                        class_id=class_.class_id,
                        primary_class_group_id=primary_group.group_id,
                        secondary_class_group_id=secondary_group.group_id if secondary_group else None,
                    )

        # 9 - Add lessons
        print("Adding lessons to class groups...")
        for class_dict in classes:
            for lesson in class_dict["lesson_info"]:
                date, start_time, end_time, lesson_type, teacher, room = lesson
                group_id = get_class_group_by_name(class_dict["class_id"], lesson_type).group_id
                lesson_ids.append(
                    add_lesson(
                        group_id=group_id,
                        date=date,
                        start_time=start_time,
                        end_time=end_time,
                        room=room,
                        teacher_id=get_user_by_name(*teacher).user_id,
                    )
                )

        # 10 - Subscribe all students and admin to all assos by default
        print("Subscribing students to assos...")
        for user_id in student_ids + admin_ids:
            for asso_id in asso_ids:
                subscribe_to_asso(user_id, asso_id)

        # 11 - Add association events
        print("Adding asso events...")
        # Tribu meeting every monday at 18h
        asso_id = asso_ids[0]
        date_range = pd.date_range(start="2023-09-01", end="2024-04-30", freq="W-MON")
        for date in date_range:
            add_event(
                asso_id,
                "Réunion",
                date,
                "18:00",
                "19:00",
                "Subscribers",
            )

        # EJE meeting every tuesday at 17h
        asso_id = asso_ids[1]
        date_range = pd.date_range(start="2023-09-01", end="2024-04-30", freq="W-TUE")
        for date in date_range:
            add_event(
                asso_id,
                "Réunion",
                date,
                "17:00",
                "18:00",
                "Subscribers",
            )

        # 12 - Add grades
        print("Adding grades...")
        for student_id in student_ids:
            for class_id in class_ids:
                # Choose a random grade between 7 and 19
                grade_value = random.randint(14, 38) / 2
                add_grade(student_id, class_id, grade_value)

        # 13 - Add homework to half of the classes, randomly
        print("Adding homework...")
        for class_id in class_ids:
            if random.random() < 0.5:
                # Iterate over the lessons of the class
                class_ = get_class_by_id(class_id)
                for lesson in class_.main_group().lessons:
                    # Add homework to the lesson
                    if random.random() < 0.2:
                        add_homework_to_class(
                            content=random.choice(homework_contents),
                            class_id=class_id,
                            due_date=lesson.date.strftime("%Y-%m-%d"),
                            due_time=lesson.start_time.strftime("%H:%M"),
                        )


if __name__ == "__main__":
    initialize_database()
