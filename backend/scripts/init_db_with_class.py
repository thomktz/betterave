import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from app.database.session import Base, engine
from app.models.class_ import Class
from app.models.student import Student
from app.database.operations import add_class

def main():
    Base.metadata.create_all(bind=engine)
    add_class(1, "Stats", 4, "DALALYAN Arnak")
    print("Database initialized successfully!")

if __name__ == "__main__":
    main()
