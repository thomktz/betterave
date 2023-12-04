"""Initialize the database with dummy data."""

import random
import json
import numpy as np
from main import app
from extensions import db
from app.operations.user_operations import add_user, get_user_by_name
from app.operations.student_operations import get_students_from_level
from app.operations.class_operations import add_class, get_classes_from_level
from app.operations.lesson_operations import add_lesson
from app.operations.class_group_operations import (
    add_class_group,
    enroll_student_in_group,
    get_class_group_by_name,
)
from app.operations.user_class_group_operations import add_user_class_group
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


def initialize_database():
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

        # 7 - Enroll students in groups
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

        # 8 - Add lessons
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


if __name__ == "__main__":
    initialize_database()
