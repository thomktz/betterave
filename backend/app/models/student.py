from extensions import db
from flask_login import UserMixin
from . import student_classes

class Student(db.Model, UserMixin):
    """SQLAlchemy object for students."""
    
    __tablename__ = "students"
    student_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(120), nullable=False)
    profile_pic = db.Column(db.String(120), nullable=True)
    level = db.Column(db.String(30), nullable=False)
    # Many-to-Many relationship with Class
    classes = db.relationship('Class', secondary=student_classes, back_populates='students')
