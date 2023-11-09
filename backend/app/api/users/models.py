"""Defines the Flask-RestX data models for serializing and deserializing user data."""

from flask_restx import fields, Model
from .namespace import api

# User model for public data
user_model = api.model(
    "User", 
    {
        "user_id": fields.Integer(description="Unique identifier"),
        "email": fields.String(required=True, description="User email address"),
        "name": fields.String(required=True, description="User first name"),
        "surname": fields.String(required=True, description="User last name"),
        "profile_pic": fields.String(description="URL to the user\"s profile picture"),
        "level": fields.String(attribute="level.value", description="User level or grade"),
        "user_type": fields.String(attribute="user_type.value", description="Type of user (e.g., student, teacher, admin)"),
    },
)

# Full user model including sensitive data
user_full_model = api.inherit(
    "UserFull", 
    user_model, 
    {
        "hashed_password": fields.String(required=True, description="User hashed password")
    }
)

class_group_model = api.model(
    "ClassGroup", 
    {
        "class_id": fields.Integer(description="Class ID"),
        "class_name": fields.String(description="Class name"),
        "primary_class_group_id": fields.Integer(description="Primary class group ID"),
        "secondary_class_group_id": fields.Integer(description="Secondary class group ID"),
        "secondary_class_group_name": fields.String(description="Secondary class group name"),
        "all_groups": fields.List(fields.String, description="All groups names")
    }
)

user_classgroups_model = api.model(
    "UserDetail", 
    {
        "id": fields.Integer(description="User ID"),
        "name": fields.String(description="First name of the user"),
        "surname": fields.String(description="Last name of the user"),
        "classgroups": fields.List(fields.Nested(class_group_model), description="List of classes associated with the user")
    }
)
