"""Flask SQLAlchemy model for a notification."""

from datetime import datetime
from betterave_backend.extensions import db


class Notification(db.Model):
    """SQLAlchemy object representing a notification."""
    print("test5")
    __tablename__ = "notification"
    notification_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.String(2048), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sent_by_user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    sender = db.relationship("User", foreign_keys=[sent_by_user_id])
    
    recipient_type = db.Column(db.String, nullable=False)
    
    recipient_users = db.relationship("User", secondary="notification_reception", back_populates="receptionned_notifications")

    #recipient_level = db.Column(db.Enum(UserLevel), nullable=True)
    #for_followers = db.Column(db.Boolean, default=False, nullable=False)

    #def send_to_followers(self):
       # """Send the notification to all followers of the sender."""
       # self.for_followers = True

    #def send_to_level(self, user_level):
        #"""Send the notification to all users of the specified level."""
       # self.recipient_level = user_level
        
        
 

