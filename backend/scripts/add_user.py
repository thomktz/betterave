"""Script to add a new user to the database."""

from main import app
from extensions import db
from app.database.operations import add_user, get_user_by_id

def add_new_user():
    print("---- Add a new user ----")
    
    name = input("Enter user's first name: ")
    surname = input("Enter user's surname: ")
    profile_pic = input("Enter user's profile picture link (or leave empty): ")
    level = input("Enter user's level (e.g., 1A, 2A, ...): ")
    user_type = input("Enter user's type (e.g., student, student_asso, teacher,admin): ")

    enrolled_classes = input("Enter class IDs the user is enrolled in (comma-separated, e.g., 1,2,3): ")
    enrolled_classes_ids = [int(cid) for cid in enrolled_classes.split(",")] if enrolled_classes else []

    user_id = add_user(name, surname, profile_pic, level, enrolled_classes_ids)
    print("user ID", user_id)

    user = get_user_by_id(user_id)
    print("---- user Details from Database ----")
    print(f"Name: {user.name} {user.surname}")
    print(f"ID: {user.user_id}")
    print(f"Email: {user.email}")
    print(f"Password (Hashed): {user.hashed_password}")

if __name__ == "__main__":
    with app.app_context():
        add_new_user()
