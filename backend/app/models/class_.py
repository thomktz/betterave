from sqlalchemy import Column, ForeignKey, Integer, String, Table

from app.database.session import Base

student_classes = Table(
    "student_classes",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.student_id")),
    Column("class_id", Integer, ForeignKey("classes.class_id")),
)


class Class(Base):
    """SQLAlchemy object for classes."""
    
    __tablename__ = "classes"
    class_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    ects_credits = Column(Integer)
    ensae_link = Column(String)
    tutor = Column(String)
