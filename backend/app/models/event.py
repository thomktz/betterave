from extensions import db


class Event(db.Model):
    """SQLAlchemy object representing a specific event organized by an association."""

    __tablename__ = "event"
    event_id = db.Column(db.Integer, primary_key=True)
    asso_id = db.Column(
        db.Integer, db.ForeignKey("user.user_id"), nullable=False
    )  # This links the event to the association.
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    participant_type = db.Column(db.String, nullable=False)

    # Relationships
    attending_users = db.relationship("User", secondary="event_attendance", back_populates="attended_events")
    association = db.relationship("User", foreign_keys=[asso_id])
