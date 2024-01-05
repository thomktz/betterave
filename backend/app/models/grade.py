"""SQLAlchemy object for Grade associated with a ClassGroup."""
from typing import Any
from extensions import db


class Grade(db.Model):
    """SQLAlchemy object for grade associated with a Class."""

    __tablename__ = "grade"
    grade_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("class.class_id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    grade = db.Column(db.Integer, nullable=False)

    def get_id(self) -> str:
        """Get the grade's ID."""
        return str(self.grade_id)

    def get_student_id(self) -> str:
        """Get the grade's student's ID."""
        return str(self.user_id)

    def get_grade(self) -> str:
        """Get the grade."""
        return str(self.grade)

    def as_dict(self) -> dict[str, Any]:
        """Return the grade as a dictionary."""
        return {
            "grade_id": self.grade_id,
            "user_id": self.user.user_id,
            "class_id": self.group_ref.class_id,
            "grade": self.grade,
        }
