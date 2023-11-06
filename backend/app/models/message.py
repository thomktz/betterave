from datetime import datetime
from extensions import db

class Message(db.Model):
    """SQLAlchemy object for messages associated with a ClassGroup."""
    
    __tablename__ = "message"
    message_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('class_group.group_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group_ref = db.relationship('ClassGroup', back_populates='messages')
    user = db.relationship('User', back_populates='messages')

    def as_dict(self):
        return {
            "message_id": self.message_id,
            "group_id": self.group_id,
            "user_id": self.user_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "user_name": self.user.name,
            "user_surname": self.user.surname,
            "user_profile_pic": self.user.profile_pic,
        }