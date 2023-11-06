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


association_subscriptions = db.Table(
    'association_subscriptions',
    db.Column('subscriber_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('asso_id', db.Integer, db.ForeignKey('user.user_id'))
)

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
    groups = db.relationship('ClassGroup', secondary="group_enrollment", back_populates='students')
    messages = db.relationship('Message', back_populates='user')
    attended_events = db.relationship('Event', secondary='event_attendance', back_populates='attending_users')
    subscriptions = db.relationship(
        'User', 
        secondary=association_subscriptions,
        primaryjoin=(user_id == association_subscriptions.c.subscriber_id),
        secondaryjoin=(user_id == association_subscriptions.c.asso_id),
        backref=db.backref('subscribers', lazy='dynamic')
    )
    
    def get_user_type(self):
        return self.user_type

    def get_id(self):
        """Necessary because UserMixin expects either an "id" argument or a "get_id" method."""
        return self.user_id