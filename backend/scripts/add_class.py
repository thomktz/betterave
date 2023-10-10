import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from app.database.operations import add_class

if __name__ == "__main__":
    print("---- Add a new class ----")
    class_id = input("Enter class ID: ")
    name = input("Enter class name: ")
    ects_credits = int(input("Enter class ECTS credits: "))
    tutor = input("Enter tutor's name: ")

    add_class(class_id, name, ects_credits, tutor)
    print(f"Class {name} added successfully!")
