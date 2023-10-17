from extensions import db

class Class(db.Model):
    """SQLAlchemy object representing an ENSAE course."""
    
    __tablename__ = "class"
    class_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ects_credits = db.Column(db.Integer, nullable=False)
    ensae_link = db.Column(db.String, nullable=False)
    backgroundColor = db.Column(db.String, nullable=True)
    
    default_teacher_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    default_teacher = db.relationship('User', foreign_keys=[default_teacher_id])
    
    # Relationships
    students = db.relationship('User', secondary='enrollment', back_populates='enrolled_classes')
    messages = db.relationship('Message', back_populates='class_ref')
    lessons = db.relationship('Lesson', back_populates='course')
    authorized_teachers = db.relationship(
        "User",
        secondary="class_authorized_teachers",
        backref="authorized_classes"
    )

    def get_id(self):
        return str(self.class_id)