from main import app, db
from app.database.operations import add_class

def initialize_database():
    with app.app_context():
        db.create_all()
        add_class(1, "Stats", 4, "DALALYAN Arnak")
        add_class(2, "Econo", 3, "SABAN Lucas")
        add_class(3, "Maths fi", 3, "ROUILLARD Pierre")
        print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
