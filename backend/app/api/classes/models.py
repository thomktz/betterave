from flask_restx import fields, Model
from .namespace import api
from app.models.enums import UserLevel

class_model = api.model("Class", {
    "class_id": fields.Integer(description="The unique identifier of the class"),
    "name": fields.String(required=True, description="The name of the class"),
    "ects_credits": fields.Integer(required=True, description="ECTS credit points for the class"),
    "ensae_link": fields.String(required=True, description="ENSAE link to the class details"),
    "level": fields.String(attribute="level.value", description="Level of the class"),
    "background_color": fields.String(description="Background color associated with the class"),
    "default_teacher_id": fields.Integer(required=True, description="The ID of the default teacher for the class")
})
