from extensions import db

# Association table for the many-to-many relationship
student_classes = db.Table(
    "student_classes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.user_id"), primary_key=True),
    db.Column("class_id", db.Integer, db.ForeignKey("classes.class_id"), primary_key=True),
)