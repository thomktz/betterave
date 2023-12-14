"""SQLAlchemy object for homework associated with a ClassGroup."""
from extensions import db


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

    def get_id(self):
        """Get the homework's ID."""
        return str(self.homework_id)

    def get_content(self):
        """Get the homework's content."""
        return str(self.content)

    def __lt__(self, other):
        """Define the '<' operator for Homework objects."""
        return (self.due_date < other.due_date) or (self.due_date == other.due_date and self.due_time < other.due_time)

    def as_dict(self):
        """Return the homework as a dictionary."""
        return {
            "homework_id": self.homework_id,
            "class_id": self.group_ref.class_id,
            "class_name": self.group_ref.class_ref.name,
            "content": self.content,
            "due_date": self.due_date,
            "due_time": self.due_time,
        }
