# type: ignore
"""SQLAlchemy object for homework associated with a ClassGroup."""
from typing import Any
from betterave_backend.extensions import db


class Homework(db.Model):
    """SQLAlchemy object for homework associated with a ClassGroup."""

    __tablename__ = "homework"
    homework_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("class_group.group_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    due_time = db.Column(db.Time, nullable=True)

    # Relationships
    group_ref = db.relationship("ClassGroup", back_populates="homework")

    def get_id(self) -> str:
        """Get the homework's ID."""
        return str(self.homework_id)

    def get_content(self) -> str:
        """Get the homework's content."""
        return str(self.content)

    def __lt__(self, other) -> bool:
        """Define the '<' operator for Homework objects."""
        if self.due_date != other.due_date:
            return self.due_date < other.due_date
        if self.due_time is None:
            return True
        if other.due_time is None:
            return False
        return self.due_time < other.due_time

    def as_dict(self) -> dict[str, Any]:
        """Return the homework as a dictionary."""
        return {
            "homework_id": self.homework_id,
            "class_id": self.group_ref.class_id,
            "class_name": self.group_ref.class_ref.name,
            "content": self.content,
            "due_date": self.due_date,
            "due_time": self.due_time,
        }
