"""
SQLAlchemy model for a class.

A class in the broadest sense is a course at ENSAE, with a name, a number of ECTS credits, etc.
Not to be confused with
- a class group, which is a subgroup of a class (Groupe de TD, Groupe d'amphi)
- a lesson, which is an actual lesson (TD, Amphi, TP, etc.) that occurs at a given time and place

"""

from backend.extensions import db
from backend.app.models.enums import UserLevel


class Class(db.Model):
    """SQLAlchemy object representing an ENSAE course."""

    __tablename__ = "class"
    class_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ects_credits = db.Column(db.Integer, nullable=False)
    ensae_link = db.Column(db.String, nullable=False)
    level = db.Column(db.Enum(UserLevel), nullable=False)
    background_color = db.Column(db.String, nullable=True)

    default_teacher_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    default_teacher = db.relationship("User", foreign_keys=[default_teacher_id])

    # Relationship to link ClassGroup
    groups = db.relationship("ClassGroup", back_populates="class_ref", lazy="dynamic")
    user_groups = db.relationship("UserClassGroup", back_populates="class_", lazy="dynamic")

    # Not type-hinted because of circular import
    def main_group(self):  # type: ignore
        """Retrieve the main group for this class."""
        return self.groups.filter_by(is_main_group=True).first()

    # Not type-hinted because of circular import
    def secondary_groups(self):  # type: ignore
        """Retrieve the secondary groups for this class."""
        return self.groups.filter_by(is_main_group=False).all()

    def get_id(self) -> str:
        """Get the ID of this class."""
        return str(self.class_id)
