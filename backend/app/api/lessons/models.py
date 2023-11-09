from flask_restx import fields
from .namespace import api
# from app.models import User, ClassGroup

class UserModel(fields.Raw):
    def format(self, value):
        return f"{value.name} {value.surname}"

class ClassGroupNameModel(fields.Raw):
    def format(self, value):
        return value.name

class ClassNameModel(fields.Raw):
    def format(self, value):
        return value.class_ref.name

class ClassBackgoundColorModel(fields.Raw):
    def format(self, value):
        return value.class_ref.background_color

lesson_model = api.model("Lesson", {
    # Endogenous fields
    "lesson_id": fields.Integer(readonly=True, description="Unique identifier of the lesson"),
    "group_id": fields.Integer(required=True, description="Identifier of the class group"),
    "date": fields.Date(required=True, description="Date of the lesson"),
    "start_time": fields.String(required=True, description="Start time of the lesson"),
    "end_time": fields.String(required=True, description="End time of the lesson"),
    "homework": fields.String(description="Homework for the lesson"),
    "room": fields.String(description="Room where the lesson takes place"),
    "teacher_id": fields.Integer(description="Identifier of the teacher for the lesson"),
    # Custom fields for related data
    "teacher_name": UserModel(attribute="teacher"),
    "class_group_name": ClassGroupNameModel(attribute="class_group"),
    "class_name": ClassNameModel(attribute="class_group"), 
    "class_background_color": ClassBackgoundColorModel(attribute="class_group"),
})