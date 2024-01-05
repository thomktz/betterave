# type: ignore
from flask_restx import Resource
from .models import fullcalendar_lesson_model, lesson_post_model
from .namespace import api
from app.operations.lesson_operations import (
    get_all_lessons,
    add_lesson,
    get_lesson_by_id,
    update_lesson,
    delete_lesson,
)
from app.decorators import require_authentication


@api.route("/")
class LessonList(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_list_with(fullcalendar_lesson_model)
    def get(self):
        """List all lessons."""
        return get_all_lessons()

    @api.doc(security="apikey")
    @require_authentication("admin", "teacher")
    @api.expect(lesson_post_model)
    def post(self):
        """Create a new lesson."""
        return add_lesson(api.payload), 201


@api.route("/<int:lesson_id>")
@api.response(404, "Lesson not found")
class LessonResource(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_with(fullcalendar_lesson_model)
    def get(self, lesson_id):
        """Fetch a lesson given its identifier."""
        lesson = get_lesson_by_id(lesson_id)
        if lesson:
            return lesson
        api.abort(404, "Lesson not found")

    @api.doc(security="apikey")
    @require_authentication("admin", "teacher")
    @api.expect(lesson_post_model)
    @api.response(204, "Lesson successfully updated")
    def put(self, lesson_id):
        """Update a lesson given its identifier."""
        if update_lesson(lesson_id, api.payload):
            return None, 204
        api.abort(400, "Could not update lesson.")

    @api.doc(security="apikey")
    @require_authentication("admin", "teacher")
    @api.response(204, "Lesson successfully deleted")
    def delete(self, lesson_id):
        """Delete a lesson given its identifier."""
        if delete_lesson(lesson_id):
            return None, 204
        api.abort(404, "Lesson not found or could not be deleted")
