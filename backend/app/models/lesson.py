from extensions import db

class Lesson(db.Model):
    """SQLAlchemy object representing a specific lesson within a class."""
    
    __tablename__ = "lesson"
    lesson_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    homework = db.Column(db.String, nullable=True)
    room = db.Column(db.String, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)

    # Relationships
    students = db.relationship('User', secondary="attendance", back_populates='registered_lessons')
    course = db.relationship('Class', back_populates='lessons')
    teacher = db.relationship('User', foreign_keys=[teacher_id])
    
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

