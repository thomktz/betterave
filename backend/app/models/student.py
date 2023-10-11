from extensions import db
from flask_login import UserMixin
from . import student_classes

class Student(db.Model, UserMixin):
    """
    SQLAlchemy object for students.
    
    Since students are the users, we inherit from flask_login's UserMixin.
    """
    
    __tablename__ = "students"
    student_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    hashed_password = db.Column(db.String(120))
    name = db.Column(db.String(80))
    surname = db.Column(db.String(120))
    profile_pic = db.Column(db.String(120), nullable=True)
    level = db.Column(db.String(30))
    # Many-to-Many relationship with Class
    classes = db.relationship('Class', secondary=student_classes, back_populates='students')
    
    def get_id(self):
        return str(self.student_id)
