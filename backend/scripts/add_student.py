import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from database.operations import add_student

def main():
    print("---- Add a new student ----")
    name = input("Enter student's first name: ")
    surname = input("Enter student's surname: ")
    profile_pic = input("Enter student's profile picture link (or leave empty): ")
    level = input("Enter student's level (e.g., Freshman): ")

    enrolled_classes = input("Enter class IDs the student is enrolled in (comma-separated, e.g., 1,2,3): ")
    enrolled_classes_ids = [int(cid) for cid in enrolled_classes.split(",")] if enrolled_classes else []

    add_student(name, surname, profile_pic, level, enrolled_classes_ids)
    print(f"Student {name} {surname} added successfully!")

if __name__ == "__main__":
    main()
