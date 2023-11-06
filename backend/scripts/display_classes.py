from main import app
from extensions import db
from app.operations.class_operations import get_all_classes



def list_classes():
    classes = get_all_classes()
    print("Students:")
    for class_ in classes:
        print(f"ID: {class_.class_id} - Name: {class_.name} {[g.name for g in class_.groups]}")
        print("Main group: ", class_.main_group().name)
        print('Other groups: ', [g.name for g in class_.secondary_groups()])

if __name__ == "__main__":
    with app.app_context():
        list_classes()

