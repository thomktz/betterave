from sqlalchemy import Column, Integer, String, ForeignKey, Table
from database.session import Base

student_classes = Table('student_classes', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.student_id')),
    Column('class_id', Integer, ForeignKey('classes.class_id'))
)

class Class(Base):
    __tablename__ = 'classes'

    class_id = Column(Integer, primary_key=True, autoincrement=False)  # Set autoincrement to False
    name = Column(String)
    ects_credits = Column(Integer)
    ensae_link = Column(String)
    tutor = Column(String)
