from extensions import db

class Lesson(db.Model):
    """SQLAlchemy object representing a specific lesson within a class."""
    
    __tablename__ = "lesson"
    lesson_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('class_group.group_id'), nullable=False)
    
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    homework = db.Column(db.String, nullable=True)
    room = db.Column(db.String, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    
    # Relationships
    # References 'class_group' instead of 'class'
    class_group = db.relationship('ClassGroup', back_populates='lessons')
    teacher = db.relationship('User', foreign_keys=[teacher_id])
    
    # Ordering methods for comparing lessons
    def __lt__(self, other):
        # Compare first by date, then by start time
        if not isinstance(other, Lesson):
            return NotImplemented
        return (self.date, self.start_time) < (other.date, other.start_time)

    def __eq__(self, other):
        # Equal if both date and start time are the same
        if not isinstance(other, Lesson):
            return NotImplemented
        return self.date == other.date and self.start_time == other.start_time
