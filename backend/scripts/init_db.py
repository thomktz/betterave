import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from app.database.session import Base, engine
from app.models.class_ import Class
from app.models.student import Student

def main():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    main()