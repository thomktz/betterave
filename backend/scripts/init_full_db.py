import random
from main import app
from extensions import db
from app.database.operations import add_class, add_student

import datetime

class TimeSlot:
    def __init__(self, date, start_time, end_time):
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f"{self.date} from {self.start_time} to {self.end_time}"

    def __lt__(self, other):
        if not isinstance(other, TimeSlot):
            return NotImplemented
        if self.date != other.date:
            return self.date < other.date
        return self.start_time < other.start_time

    def __eq__(self, other):
        if not isinstance(other, TimeSlot):
            return NotImplemented
        return self.date == other.date and self.start_time == other.start_time


def weekly_timeslot(start_date, end_date, day_of_week, start_time, end_time):
    # Convert day_of_week string to an integer (0=Monday, 6=Sunday)
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    if day_of_week.lower() not in days:
        raise ValueError("Invalid day of the week")

    day_num = days.index(day_of_week.lower())

    # Parse the start_date and end_date strings into datetime.date objects
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    time_slots = []
    current_date = start_date
    # Adjust the current_date to the next occurrence of the specified day_of_week
    while current_date.weekday() != day_num and current_date <= end_date:
        current_date += datetime.timedelta(days=1)

    # Now, keep adding time slots for each occurrence of the day_of_week until we reach the end_date
    while current_date <= end_date:
        time_slots.append(TimeSlot(current_date, start_time, end_time))
        current_date += datetime.timedelta(days=7)
    return time_slots


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
