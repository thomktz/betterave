from extensions import db

class ClassGroup(db.Model):
    __tablename__ = "class_group"
    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class.class_id"), nullable=False)
    is_main_group = db.Column(db.Boolean, default=False, nullable=False)
    
    class_ref = db.relationship("Class", back_populates="groups")    
    students = db.relationship("User", secondary="group_enrollment", back_populates="groups")
    lessons = db.relationship("Lesson", back_populates="class_group")
    messages = db.relationship("Message", back_populates="group_ref", lazy="dynamic")