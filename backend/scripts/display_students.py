from main import app
from extensions import db
from app.database.operations import get_lessons_by_student
from app.models.student import Student
from app.models.class_ import Class


def list_students():
    students = Student.query.all()
    for student in students:
        print(f"ID: {student.student_id} - Name: {student.name} {student.surname}")

def get_classes_for_student(student_id):
    student = db.session.get(Student, student_id)
    if not student:
        print("Student not found!")
        return

    print(f"Classes for {student.name} {student.surname}:")
    for class_ in student.classes:
        print(f" - {class_.name}")
        
        
def get_calendar(student_id):
    lessons = get_lessons_by_student(student_id)
    print(f"Lessons for student {student_id}:")
    for lesson in lessons:
        print(f" - {lesson.class_ref.name} - {lesson.start_time} - {lesson.end_time}")
    

if __name__ == "__main__":
    with app.app_context():
        list_students()
        student_id = int(input("Enter the ID of the student to view their classes: "))
        get_classes_for_student(student_id)
        get_calendar(student_id)

