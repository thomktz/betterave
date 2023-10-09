from sqlalchemy import Column, Integer, String
from app.database.session import Base

class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    surname = Column(String)
    profile_pic = Column(String)
    level = Column(String)
