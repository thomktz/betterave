from extensions import db
from flask_login import UserMixin
from . import user_classes

class User(db.Model, UserMixin):
    """
    SQLAlchemy object for students.
    
    Since students are the users, we inherit from flask_login's UserMixin.
    """
    
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    hashed_password = db.Column(db.String(120))
    name = db.Column(db.String(80))
    surname = db.Column(db.String(120))
    profile_pic = db.Column(db.String(120), nullable=True)
    level = db.Column(db.String(30))
    user_type = db.Column(db.String(30))  # "student","student_asso","teacher","admin"

    # if user_type == "student":
    #     # Many-to-Many relationship with Class
    classes = db.relationship('Class', secondary=user_classes, back_populates='students')
    
    def get_id(self):
        return str(self.user_id)  ## Besoin de cette méthode ? déjà implémentée dans UserMixin
    
    def get_user_type(self):
        return self.user_type
