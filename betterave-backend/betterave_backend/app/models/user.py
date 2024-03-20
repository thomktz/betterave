"""SQLAlchemy object representing a user with different roles and levels."""

from typing import Any
from flask_login import UserMixin
from betterave_backend.extensions import db
from betterave_backend.app.models.enums import UserLevel, UserType


association_subscriptions = db.Table(
    "association_subscriptions",
    db.Column("subscriber_id", db.Integer, db.ForeignKey("user.user_id")),
    db.Column("asso_id", db.Integer, db.ForeignKey("user.user_id")),
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
    groups = db.relationship("ClassGroup", secondary="group_enrollment", back_populates="students")
    class_groups = db.relationship("UserClassGroup", back_populates="user", lazy="dynamic")
    messages = db.relationship("Message", back_populates="user")
    lessons_taught = db.relationship("Lesson", back_populates="teacher", lazy="dynamic")
    attended_events = db.relationship("Event", secondary="event_attendance", back_populates="attending_users")
    receptionned_notifications = db.relationship("Notification", secondary="notification_reception", back_populates="recipient_users")
    subscriptions = db.relationship(
        "User",
        secondary=association_subscriptions,
        primaryjoin=(user_id == association_subscriptions.c.subscriber_id),
        secondaryjoin=(user_id == association_subscriptions.c.asso_id),
        backref=db.backref("subscribers", lazy="dynamic"),
    )

    def get_user_type(self) -> UserType:
        """Get the user type."""
        return self.user_type

    def get_id(self) -> int:
        """Necessary because UserMixin expects either an "id" argument or a "get_id" method."""
        return self.user_id  # type: ignore

    def as_dict(self) -> dict[str, Any]:
        """Convert the SQLAlchemy object into a dictionary."""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "profile_pic": self.profile_pic,
            "level": self.level.value,
            "user_type": self.user_type.value,
        }

    @property
    def is_student(self) -> bool:
        """Return whether the user is a student."""
        return self.user_type == UserType.STUDENT  # type: ignore

    @property
    def is_teacher(self) -> bool:
        """Return whether the user is a teacher."""
        return self.user_type == UserType.TEACHER  # type: ignore

    @property
    def is_asso(self) -> bool:
        """Return whether the user is an association."""
        return self.user_type == UserType.ASSO  # type: ignore

    @property
    def is_admin(self) -> bool:
        """Return whether the user is an admin."""
        return self.user_type == UserType.ADMIN  # type: ignore
