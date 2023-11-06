from main import app
from extensions import db
from app.operations.user_operations import get_user_by_id
from app.operations.student_operations import get_all_students, get_student_lessons



def list_students():
    students = get_all_students()
    print("Students:")
    for student in students:
        print(f"ID: {student.user_id} - Name: {student.name} {student.surname}")

def get_classes_for_student(user_id):
    student = get_user_by_id(user_id)
    if not student:
        print("Student not found!")
        return

    print(f"Classes for {student.name} {student.surname}:")
    for group in student.groups:
        print(f" - {group.class_ref.name} {group.name}")
        
        
def get_calendar(user_id):
    lessons = get_student_lessons(user_id)
    print(f"Lessons for User {user_id}:")
    for lesson in sorted(lessons):
        print(f" - {lesson.class_group.class_ref.name} - {lesson.class_group.name} - {lesson.date} - {lesson.end_time}")
    

if __name__ == "__main__":
    with app.app_context():
        list_students()
        user_id = int(input("Enter the ID of the User to view their classes: "))
        get_classes_for_student(user_id)
        get_calendar(user_id)

