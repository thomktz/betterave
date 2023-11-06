from main import app
from extensions import db
from app.operations.user_operations import get_user_by_id
from app.operations.student_operations import get_all_students, get_student_lessons



def list_students():
    students = get_all_students()
    print("Students:")
    for student in students:
        print(f"ID: {student.user_id} - Name: {student.name} {student.surname}")
        
def get_user_details(user_id):
    student = get_user_by_id(user_id)
    if not student:
        print("Student not found!")
        return

    print(f"Details for {student.name} {student.surname}:\n")

    # List of ClassGroups
    print("# LIST OF ClassGroups:")
    for group in student.groups:
        class_name = group.class_ref.name if group.class_ref else "No Class"
        print(f"- {class_name} {group.name}")

    print("\n# LIST OF UserClassGroups")
    # List of UserClassGroups
    for ucg in student.class_groups:
        class_name = ucg.class_.name if ucg.class_ else "No Class"
        primary_group_name = ucg.primary_class_group.name if ucg.primary_class_group else "No Primary Group"
        secondary_group_name = ucg.secondary_class_group.name if ucg.secondary_class_group else "No Secondary Group"
        print(f"- Class: {class_name}, Primary Group: {primary_group_name}, Secondary Group: {secondary_group_name}")


if __name__ == "__main__":
    with app.app_context():
        list_students()
        user_id = int(input("Enter the ID of the User to view their classes: "))
        get_user_details(user_id)

