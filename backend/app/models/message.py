from datetime import datetime
from extensions import db

class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # relationships
    class_ref = db.relationship('Class', backref=db.backref('messages', lazy=True))
    student = db.relationship('Student', backref=db.backref('messages', lazy=True))

    def as_dict(self):
        return {
            "message_id": self.message_id,
            "class_id": self.class_id,
            "student_id": self.student_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "student_name": self.student.name,
            "student_surname": self.student.surname,
            "student_profile_pic": self.student.profile_pic,
        }