"""Flask SQLAlchemy model for Chat messages associated with a ClassGroup.""" ""

from typing import Any
from datetime import datetime
from betterave_backend.extensions import db


class Message(db.Model):
    """SQLAlchemy object for Chat messages associated with a ClassGroup."""

    __tablename__ = "message"
    message_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("class_group.group_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    group_ref = db.relationship("ClassGroup", back_populates="messages")
    user = db.relationship("User", back_populates="messages")

    def as_dict(self) -> dict[str, Any]:
        """Return the message as a dictionary."""
        return {
            "message_id": self.message_id,
            "group_id": self.group_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "sender_details": {
                "user_id": self.user.user_id,
                "name": self.user.name,
                "surname": self.user.surname,
                "profile_pic": self.user.profile_pic,
            },
        }
