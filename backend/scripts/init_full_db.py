import random
import datetime
from main import app
from extensions import db
from app.database.operations import add_class, add_student, add_lesson



def add_weekly_lessons(class_id, start_date, end_date, day_of_week, start_time, end_time, homework=None, room=None, tutor=None):
    # Convert day_of_week string to an integer (0=Monday, 6=Sunday)
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    if day_of_week.lower() not in days:
        raise ValueError("Invalid day of the week", day_of_week)

    day_num = days.index(day_of_week.lower())

    # Parse the start_date and end_date strings into datetime.date objects
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    lesson_ids = []
    current_date = start_date
    # Adjust the current_date to the next occurrence of the specified day_of_week
    while current_date.weekday() != day_num and current_date <= end_date:
        current_date += datetime.timedelta(days=1)

    # Now, keep adding lessons for each occurrence of the day_of_week until we reach the end_date
    while current_date <= end_date:
        # Add a new lesson for the current_date
        lesson_id = add_lesson(class_id, current_date, start_time, end_time, homework, room, tutor)
        lesson_ids.append(lesson_id)

        # Jump to the next week (next occurrence of the day_of_week)
        current_date += datetime.timedelta(days=7)

    return lesson_ids

classes = [
    {
        "class_id": 1,
        "name": "Introduction à la microéconomie",
        "ects_credits": 3,
        "tutor": "LINNEMER Laurent",
        "lesson_times": [
            ("monday", "09:00:00", "10:30:00"),
            ("monday", "10:45:00", "12:15:00"),
        ],
        "backgroundColor": "#dbb1bc",
    },{
        "class_id": 2,
        "name": "Introduction à la macroéconomie",
        "ects_credits": 3,
        "tutor": "LOISEL Olivier",
        "lesson_times": [
            ("monday", "14:15:00", "15:45:00"),
            ("monday", "16:00:00", "17:30:00"),
        ],
        "backgroundColor": "#d3c4e3",
    },{
        "class_id": 4,
        "name": "Microéconomie 1 (FR)",
        "ects_credits": 4,
        "tutor": "CHONÉ Philippe",
        "lesson_times": [
            ("tuesday", "09:00:00", "10:30:00"),
            ("tuesday", "10:45:00", "12:15:00"),
        ],
        "backgroundColor": "#8f95d3",
    },{
        "class_id": 5,
        "name": "Macroéconomie 1 (FR)",
        "ects_credits": 4,
        "tutor": "LOISEL Olivier",
        "lesson_times": [
            ("tuesday", "14:15:00", "15:45:00"),
            ("tuesday", "16:00:00", "17:30:00"),
        ],
        "backgroundColor": "#45b69c",
    },{
        "class_id": 6,
        "name": "Théorie des jeux",
        "ects_credits": 2.5,
        "tutor": "FÉVRIER Philippe",
        "lesson_times": [
            ("thursday", "09:00:00", "10:30:00"),
            ("thursday", "10:45:00", "12:15:00"),
        ],
        "backgroundColor": "#D1D0A3",
    },{
        "class_id": 7,
        "name": "Infrastructures et systèmes logiciels",
        "ects_credits": 3,
        "tutor": "CHANCEL Antoine",
        "lesson_times": [
            ("thursday", "14:15:00", "15:45:00"),
            ("thursday", "16:00:00", "17:30:00"),
        ],
        "backgroundColor": "#446BC5",
    },
]

last_names = [
    "Adams", "Baker", "Clark", "Davis", "Evans", "Frank",
    "Ghosh", "Hills", "Irwin", "Jones", "Klein", "Lopez", 
    "Mason", "Nalty", "Ochoa", "Patel", "Quinn", "Reily", 
    "Smith", "Trott", "Usman", "Valdo", "White", "Xiang", 
    "Yakub", "Zafar", "Kientz", "Dechaux"
]

first_names = [
    "Alice", "Bob", "Carol", "Dave", "Eve", "Fred", 
    "Grace", "Hal", "Isaac", "Julia", "Karl", "Lara", 
    "Max", "Nora", "Oscar", "Paul", "Quinn", "Rob", 
    "Susan", "Tom", "Ursula", "Victor", "Wendy", "Xavier", 
    "Yara", "Zack", "Thomas", "Claire"
]



class_ids = list(set([class_["class_id"] for class_ in classes]))

def initialize_database():
    with app.app_context():
        db.create_all()
        for class_ in classes:
            add_class(**class_)
            for lesson in class_["lesson_times"]:
                add_weekly_lessons(class_["class_id"], "2023-10-01", "2023-12-31", *lesson, room=random.randint(2001, 2048))
            
        for i in range(27):
            add_student(
                name=first_names[i],
                surname=last_names[i],
                profile_pic=f"photos/{first_names[i]}{last_names[i]}.jpg",
                level=str(random.randint(1, 3))+"A",
                enrolled_classes_ids=random.sample(class_ids, random.randint(3, len(class_ids))),
            )
        print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
