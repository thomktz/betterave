from flask_restx import fields
from .namespace import api

class_model = api.model(
    "Class",
    {
        "class_id": fields.Integer(description="The unique identifier of the class"),
        "name": fields.String(required=True, description="The name of the class"),
        "ects_credits": fields.Integer(required=True, description="ECTS credit points for the class"),
        "ensae_link": fields.String(required=True, description="ENSAE link to the class details"),
        "level": fields.String(attribute="level.value", description="Level of the class"),
        "background_color": fields.String(description="Background color associated with the class"),
        "default_teacher_id": fields.Integer(required=True, description="The ID of the default teacher for the class"),
    },
)

homework_model = api.model(
    "Homework",
    {
        "homework_id": fields.Integer(readonly=True, description="The unique identifier of a homework"),
        "class_id": fields.Integer(required=True, description="The ID of the class the homework belongs to"),
        "class_name": fields.String(readonly=True, description="The name of the class the homework belongs to"),
        "content": fields.String(required=True, description="The content/description of the homework"),
        "due_date": fields.Date(required=True, description="The due date of the homework"),
        "due_time": fields.String(
            required=False,
            description="The due time of the homework (expected format HH:MM)",
        ),
    },
)

homework_post_model = api.model(
    "HomeworkPost",
    {
        "content": fields.String(required=True, description="The content/description of the new homework"),
        "due_date": fields.Date(required=True, description="The due date of the new homework"),
        "due_time": fields.String(
            required=False,
            description="The due time of the homework (expected format HH:MM)",
        ),
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
