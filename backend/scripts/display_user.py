from main import app
from extensions import db
from app.database.operations import get_lessons_by_user
from backend.app.models.user import User
from app.models.class_ import Class


def list_users():
    users = user.query.all()
    for user in users:
        print(f"ID: {user.user_id} - Name: {user.name} {user.surname}")

def get_classes_for_user(user_id):
    user = db.session.get(user, user_id)
    if not user:
        print("User not found!")
        return

    print(f"Classes for {user.name} {user.surname}:")
    for class_ in user.classes:
        print(f" - {class_.name}")
        
        
def get_calendar(user_id):
    lessons = get_lessons_by_user(user_id)
    print(f"Lessons for User {user_id}:")
    for lesson in lessons:
        print(f" - {lesson.class_ref.name} - {lesson.start_time} - {lesson.end_time}")
    

if __name__ == "__main__":
    with app.app_context():
        list_users()
        user_id = int(input("Enter the ID of the User to view their classes: "))
        get_classes_for_user(user_id)
        get_calendar(user_id)

