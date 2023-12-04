from extensions import db

group_enrollment = db.Table(
    "group_enrollment",
    db.Column("student_id", db.Integer, db.ForeignKey("user.user_id"), primary_key=True),
    db.Column("group_id", db.Integer, db.ForeignKey("class_group.group_id"), primary_key=True),
)

event_attendance = db.Table(
    "event_attendance",
    db.Column("user_id", db.Integer, db.ForeignKey("user.user_id")),
    db.Column("event_id", db.Integer, db.ForeignKey("event.event_id")),
)
