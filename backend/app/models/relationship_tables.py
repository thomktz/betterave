from extensions import db

# Association Table for Student-Enrolled-Classes Relationship
student_classes = db.Table(
    'enrollment',
    db.Column('student_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('class.class_id'), primary_key=True)
)

# Association Table for Student-Attended-Lessons Relationship
student_lessons = db.Table(
    'attendance',
    db.Column('student_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.lesson_id'), primary_key=True)
)

class_authorized_teachers = db.Table(
    'class_authorized_teachers',
    db.Column('teacher_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('class.class_id'), primary_key=True)
)

event_attendance = db.Table('event_attendance',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'))
)