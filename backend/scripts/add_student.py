"""Script to add a new student to the database."""

from main import app
from extensions import db
from app.database.operations import add_student, get_student_by_id

def add_new_student():
    print("---- Add a new student ----")
    
    name = input("Enter student's first name: ")
    surname = input("Enter student's surname: ")
    profile_pic = input("Enter student's profile picture link (or leave empty): ")
    level = input("Enter student's level (e.g., 1A, 2A, ...): ")

    enrolled_classes = input("Enter class IDs the student is enrolled in (comma-separated, e.g., 1,2,3): ")
    enrolled_classes_ids = [int(cid) for cid in enrolled_classes.split(",")] if enrolled_classes else []

    student_id = add_student(name, surname, profile_pic, level, enrolled_classes_ids)
    print("Student ID", student_id)

    student = get_student_by_id(student_id)
    print("---- Student Details from Database ----")
    print(f"Name: {student.name} {student.surname}")
    print(f"ID: {student.student_id}")
    print(f"Email: {student.email}")
    print(f"Password (Hashed): {student.hashed_password}")

if __name__ == "__main__":
    with app.app_context():
        add_new_student()
