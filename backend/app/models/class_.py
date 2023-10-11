from extensions import db
from . import student_classes

class Class(db.Model):
    """SQLAlchemy object for classes."""
    
    __tablename__ = "classes"
    class_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String)
    ects_credits = db.Column(db.Integer)
    ensae_link = db.Column(db.String, nullable=True)
    tutor = db.Column(db.String, nullable=True)
    backgroundColor = db.Column(db.String, nullable=True)
    
    # Many-to-Many relationship with User
    students = db.relationship('User', secondary=student_classes, back_populates='classes')
    # One-to-Many relationship with Lesson
    lessons = db.relationship('Lesson', back_populates='class_ref')


    def get_id(self):
        return str(self.class_id)