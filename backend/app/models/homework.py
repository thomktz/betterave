from datetime import datetime
from extensions import db

class Homework(db.Model):
    """SQLAlchemy object for homeworks associated with a ClassGroup."""
    
    __tablename__ = "homework"
    homework_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('class_group.group_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    #group_ref = db.relationship('ClassGroup', back_populates='homeworks')
    #user = db.relationship('User', back_populates='messages')

    def get_id(self):
        return str(self.homework_id)
    
    def get_content(self):
        return str(self.content)
    
    def as_dict(self):
        return {
            "homework_id": self.homework_id,
            "group_id": self.group_id,
            "content": self.content,
            "due_date": self.due_date
        }