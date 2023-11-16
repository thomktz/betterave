from flask_restx import fields
from .namespace import api

class_group_model = api.model("ClassGroup", {
    "group_id": fields.Integer(readonly=True, description="The unique identifier of the class group"),
    "name": fields.String(required=True, description="The name of the class group"),
    "class_id": fields.Integer(required=True, description="The identifier of the class"),
    "is_main_group": fields.Boolean(default=False, description="Indicates if this is the main group for the class")
})

sender_details_model = api.model("SenderDetails", {
    "user_id": fields.Integer(description="The unique identifier of the user"), 
    "name": fields.String(description="The name of the user"),
    "surname": fields.String(description="The surname of the user"),
    "profile_pic": fields.String(description="The profile picture of the user")
})

message_model = api.model("Message", {
    "message_id": fields.Integer(readonly=True, description="The unique identifier of a message"),
    "group_id": fields.Integer(required=True, description="The identifier of the class group associated with the message"),
    "content": fields.String(required=True, description="The content of the message"),
    "timestamp": fields.DateTime(required=True, description="The timestamp of the message"),
    "sender_details": fields.Nested(sender_details_model, description="The details of the user who posted the message")
})

homework_model = api.model("Homework", {
    "homework_id": fields.Integer(readonly=True, description="The unique identifier of a homework"),
   # "group_id": fields.Integer(required=True, description="The identifier of the class group associated with the message"),
   # "content": fields.String(required=True, description="The content/description of the homework"),
   # "due_date": fields.DateTime(required=True, description="The due date of the homework")
})

homework_post_model = api.model("HomeworkPost", {
    "content": fields.String(required=True, description="The content/description of the new homework"),
})

message_post_model = api.model("MessagePost", {
    "content": fields.String(required=True, description="The content of the new message"),
})