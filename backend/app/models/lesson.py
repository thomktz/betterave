from extensions import db

class Lesson(db.Model):
    """SQLAlchemy object for lessons."""
    
    __tablename__ = "lessons"
    lesson_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    homework = db.Column(db.String)
    room = db.Column(db.String)
    tutor = db.Column(db.String, nullable=True)

    # Relationship to the Class model
    class_ref = db.relationship("Class", back_populates="lessons")
    
    # Ordering methods
    def __lt__(self, other):
        if not isinstance(other, Lesson):
            return NotImplemented
        if self.date != other.date:
            return self.date < other.date
        return self.start_time < other.start_time

    def __eq__(self, other):
        if not isinstance(other, Lesson):
            return NotImplemented
        return self.date == other.date and self.start_time == other.start_time

