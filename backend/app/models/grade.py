"""SQLAlchemy object for Grade associated with a ClassGroup."""
from extensions import db


class Grade(db.Model):
    """SQLAlchemy object for grade associated with a ClassGroup."""

    __tablename__ = "grade"
    grade_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("class_group.group_id"), nullable=False)
    grade = db.Column(db.Integer, nullable=False)

    # Relationships
    group_ref = db.relationship("ClassGroup", back_populates="grade")

    def get_id(self):
        """Get the grade's ID."""
        return str(self.grade_id)

    def get_grade(self):
        """Get the grade"""
        return str(self.grade)
    
    def as_dict(self):
        """Return the grade as a dictionary."""
        return {
            "grade_id": self.grade_id,
            "class_id": self.group_ref.class_id,
            "class_name": self.group_ref.class_ref.name,
            "grade": self.grade
        }
