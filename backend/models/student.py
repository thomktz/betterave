from sqlalchemy import Column, Integer, String
from database.session import Base

class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    profile_pic = Column(String)
    level = Column(String)
