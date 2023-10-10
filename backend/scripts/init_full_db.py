import random
from main import app
from extensions import db
from app.database.operations import add_class, add_student

classes = [
    {
        "class_id": 1,
        "name": "Introduction à la microéconomie",
        "ects_credits": 3,
        "tutor": "LINNEMER Laurent",
    },{
        "class_id": 2,
        "name": "Introduction à la macroéconomie",
        "ects_credits": 3,
        "tutor": "LOISEL Olivier",
    },{
        "class_id": 4,
        "name": "Microéconomie 1 (FR)",
        "ects_credits": 4,
        "tutor": "CHONÉ Philippe",
    },{
        "class_id": 5,
        "name": "Macroéconomie 1 (FR)",
        "ects_credits": 4,
        "tutor": "LOISEL Olivier",
    },{
        "class_id": 6,
        "name": "Théorie des jeux",
        "ects_credits": 2.5,
        "tutor": "FÉVRIER Philippe",
    },{
        "class_id": 7,
        "name": "Infrastructures et systèmes logiciels",
        "ects_credits": 3,
        "tutor": "CHANCEL Antoine",
    },
]

last_names = [
    "Adams", "Baker", "Clark", "Davis", "Evans", "Frank",
    "Ghosh", "Hills", "Irwin", "Jones", "Klein", "Lopez", 
    "Mason", "Nalty", "Ochoa", "Patel", "Quinn", "Reily", 
    "Smith", "Trott", "Usman", "Valdo", "White", "Xiang", 
    "Yakub", "Zafar", "Kientz",
]

first_names = [
    "Alice", "Bob", "Carol", "Dave", "Eve", "Fred", 
    "Grace", "Hal", "Isaac", "Julia", "Karl", "Lara", 
    "Max", "Nora", "Oscar", "Paul", "Quinn", "Rob", 
    "Susan", "Tom", "Ursula", "Victor", "Wendy", "Xavier", 
    "Yara", "Zack", "Thomas",
]

class_ids = list(set([class_["class_id"] for class_ in classes]))

def initialize_database():
    with app.app_context():
        db.create_all()
        for class_ in classes:
            add_class(**class_)
        for i in range(27):
            add_student(
                name=first_names[i],
                surname=last_names[i],
                profile_pic=f"photos/{first_names[i]}{last_names[i]}.jpg",
                level=str(random.randint(1, 3))+"A",
                enrolled_classes_ids=random.sample(class_ids, random.randint(1, len(class_ids))),
            )
        print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
