from enum import Enum

from extensions import db
from flask_login import UserMixin


class UserType(Enum):
    STUDENT = "student"
    ASSO = "asso" # Shared account between association members
    TEACHER = "teacher"
    ADMIN = "admin"

class UserLevel(Enum):
    _1A = "1A"
    _2A = "2A"
    _3A = "3A"
    NA = "N/A" # Not applicable, for teachers, assos and admins


class User(db.Model, UserMixin):
    """SQLAlchemy object representing a user with different roles and levels."""
    
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(120), nullable=False)
    profile_pic = db.Column(db.String(120), nullable=True)
    level = db.Column(db.Enum(UserLevel), nullable=False)
    user_type = db.Column(db.Enum(UserType), nullable=False)
    
    # Mainly for assos
    linkedin = db.Column(db.String, nullable=True)
    website = db.Column(db.String, nullable=True)

    # Relationships
    enrolled_classes = db.relationship('Class', secondary='enrollment', back_populates='students')
    registered_lessons = db.relationship('Lesson', secondary='attendance', back_populates='students')
    messages = db.relationship('Message', back_populates='user')
    
    def get_user_type(self):
        return self.user_type

    def get_id(self):
        """Necessary because UserMixin expects either an "id" argument or a "get_id" method."""
        return self.user_id