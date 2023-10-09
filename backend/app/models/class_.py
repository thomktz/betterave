from extensions import db
from . import student_classes

class Class(db.Model):
    """SQLAlchemy object for classes."""
    
    __tablename__ = "classes"
    class_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String)
    ects_credits = db.Column(db.Integer)
    ensae_link = db.Column(db.String)
    tutor = db.Column(db.String)
    # Many-to-Many relationship with Student
    students = db.relationship('Student', secondary=student_classes, back_populates='classes')
