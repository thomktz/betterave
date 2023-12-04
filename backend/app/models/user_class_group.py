from extensions import db

class UserClassGroup(db.Model):
    __tablename__ = "user_class_group"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class.class_id"), nullable=False)
    primary_class_group_id = db.Column(db.Integer, db.ForeignKey("class_group.group_id"), nullable=True)
    secondary_class_group_id = db.Column(db.Integer, db.ForeignKey("class_group.group_id"), nullable=True)

    # Relationships
    user = db.relationship("User", back_populates="class_groups")
    class_ = db.relationship("Class", back_populates="user_groups")
    primary_class_group = db.relationship("ClassGroup", foreign_keys=[primary_class_group_id])
    secondary_class_group = db.relationship("ClassGroup", foreign_keys=[secondary_class_group_id])
