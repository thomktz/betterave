from datetime import datetime
from flask_restx import fields
from .namespace import api


fullcalendar_lesson_model = api.model(
    "Lesson",
    {
        "id": fields.String(
            attribute=lambda x: f"lesson_{x.lesson_id}",
            description="A unique identifier for the lesson prefixed with 'lesson_'",
        ),
        "group_id": fields.Integer(
            attribute=lambda x: x.class_group.class_id,
            description="The identifier of the class group, used for associating events with resources",
        ),
        "start": fields.DateTime(
            dt_format="iso8601",
            attribute=lambda x: datetime.combine(x.date, x.start_time).isoformat(),
            description="The start time of the lesson in ISO8601 format",
        ),
        "end": fields.DateTime(
            dt_format="iso8601",
            attribute=lambda x: datetime.combine(x.date, x.end_time).isoformat(),
            description="The end time of the lesson in ISO8601 format",
        ),
        "title": fields.String(
            attribute=lambda x: x.class_group.class_ref.name,
            description="The name of the class associated with the lesson",
        ),
        "type": fields.String(
            attribute=lambda x: x.class_group.name,
            description="The name of the class group",
        ),
        "backgroundColor": fields.String(
            attribute=lambda x: x.class_group.class_ref.background_color,
            description="The background color associated with the class for calendar display",
        ),
        "room": fields.String(attribute="room", description="The room in which the lesson takes place"),
        "teacher": fields.String(
            attribute=lambda x: f"{x.teacher.name} {x.teacher.surname}",
            description="The full name of the teacher conducting the lesson",
        ),
        "lesson_id": fields.Integer(
            attribute="lesson_id",
            description="The internal unique identifier of the lesson",
        ),
        "class_id": fields.Integer(
            attribute=lambda x: x.class_group.class_id,
            description="The internal unique identifier of the class",
        ),
        "homework": fields.String(
            attribute="homework",
            description="Details of the homework assigned for the lesson",
        ),
    },
)

lesson_post_model = api.model(
    "LessonPost",
    {
        "group_id": fields.Integer(
            required=True,
            description="The identifier of the class group associated with the lesson",
        ),
        "date": fields.Date(required=True, description="The date on which the lesson will take place"),
        "start_time": fields.String(
            required=True,
            description="The start time of the lesson (expected format HH:MM)",
        ),
        "end_time": fields.String(
            required=True,
            description="The end time of the lesson (expected format HH:MM)",
        ),
        "room": fields.String(description="The room in which the lesson is scheduled to take place"),
        "teacher_id": fields.Integer(description="The identifier of the teacher conducting the lesson"),
        "homework": fields.String(description="Any homework assigned for this lesson"),
    },
)
