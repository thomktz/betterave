from extensions import db

class Lesson(db.Model):
    __tablename__ = "lessons"
    lesson_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    homework = db.Column(db.String, nullable=True)
    # Foreign Key to link a lesson to a class
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)
    # Relation to the Class model
    class_ = db.relationship('Class', back_populates='lessons')
