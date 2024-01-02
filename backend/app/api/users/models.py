"""Defines the Flask-RestX data models for serializing and deserializing user data."""

from flask_restx import fields
from .namespace import api

user_model = api.model(
    "User",
    {
        "user_id": fields.Integer(description="Unique identifier"),
        "email": fields.String(required=True, description="User email address"),
        "name": fields.String(required=True, description="User first name"),
        "surname": fields.String(required=True, description="User last name"),
        "profile_pic": fields.String(description='URL to the user"s profile picture'),
        "level": fields.String(attribute="level.value", description="User level or grade"),
        "user_type": fields.String(
            attribute="user_type.value",
            description="Type of user (e.g., student, teacher, admin)",
        ),
    },
)

user_post_model = api.model(
    "UserPost",
    {
        "name": fields.String(required=True, description="User first name"),
        "surname": fields.String(required=True, description="User last name"),
        "email_override": fields.String(required=False, description="User email address"),
        "level": fields.String(required=True, description="User level or grade"),
        "user_type": fields.String(required=True, description="Type of user (e.g., student, teacher, admin)"),
        "password_override": fields.String(required=True, description="User password"),
    },
)

class_group_model = api.model(
    "ClassGroup",
    {
        "class_id": fields.Integer(description="Class ID"),
        "class_name": fields.String(description="Class name"),
        "class_ects": fields.Integer(description="Class ECTS"),
        "primary_class_group_id": fields.Integer(description="Primary class group ID"),
        "secondary_class_group_id": fields.Integer(description="Secondary class group ID"),
        "secondary_class_group_name": fields.String(description="Secondary class group name"),
        "all_groups": fields.List(fields.String, description="All groups names"),
    },
)

user_classgroups_model = api.model(
    "UserDetail",
    {
        "id": fields.Integer(description="User ID"),
        "name": fields.String(description="First name of the user"),
        "surname": fields.String(description="Last name of the user"),
        "level": fields.String(description="User level (1A, 2A, 3A)"),
        "classgroups": fields.List(
            fields.Nested(class_group_model),
            description="List of classes associated with the user",
        ),
    },
)

asso_model = api.model(
    "Asso",
    {
        "user_id": fields.Integer(description="Unique identifier"),
        "email": fields.String(required=True, description="User email address"),
        "name": fields.String(required=True, description="User first name"),
        "profile_pic": fields.String(description='URL to the user"s profile picture'),
        "user_type": fields.String(
            attribute="user_type.value",
            description="Type of user (e.g., student, teacher, admin)",
        ),
        "linkedin": fields.String(description='URL to the asso"s LinkedIn page', required=False),
        "website": fields.String(description='URL to the asso"s website', required=False),
    },
)


grades_model = api.model(
    "Grade",
    {
        "grade_id": fields.Integer(readonly=True, description="The unique identifier of a grade"),
        "class_id": fields.Integer(required=True, description="The ID of the class the grade belongs to"),
        "student_id": fields.Integer(required=True, description="The ID of the student receiving the grade"),
        "grade": fields.String(required=True, description="The value of the grade"),
    },
)

grades_post_model = api.model(
    "GradePost",
    {
        "student_id": fields.Integer(required=True, description="The ID of the student receiving the grade"),
        "grade": fields.String(required=True, description="The value of the grade"),
    },
)
