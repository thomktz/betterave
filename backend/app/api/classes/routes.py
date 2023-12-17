from flask_restx import Resource
from flask_login import current_user
from .models import class_model, homework_model, homework_post_model
from .namespace import api
from app.operations.class_operations import (
    add_class,
    get_class_by_id,
    get_all_classes,
    update_class,
    delete_class,
    get_classes_from_level,
    get_classes_from_teacher
)
from app.operations.message_operations import get_class_messages, add_class_message
from app.api.class_groups.models import message_model, message_post_model
from app.operations.homework_operations import get_class_homework, add_homework_to_class
from app.models import UserLevel
from app.decorators import require_authentication


@api.route("/")
class ClassList(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_list_with(class_model)
    def get(self):
        """List all classes."""
        return get_all_classes()

    @api.doc(security="apikey")
    @require_authentication("admin", "teacher")
    @api.expect(class_model)
    def post(self):
        """Create a new class."""
        return add_class(api.payload), 201


@api.route("/<int:class_id>")
@api.response(404, "Class not found")
class ClassResource(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_with(class_model)
    def get(self, class_id):
        """Fetch a class given its identifier."""
        cls = get_class_by_id(class_id)
        if cls is None:
            api.abort(404, "Class not found")
        return cls

    @api.doc(security="apikey")
    @require_authentication("admin", "teacher")
    @api.expect(class_model)
    @api.response(204, "Class updated successfully")
    def put(self, class_id):
        """Update a class given its identifier."""
        update_class(class_id, api.payload)
        return None, 204

    @api.doc(security="apikey")
    @require_authentication("admin", "teacher")
    @api.response(204, "Class deleted successfully")
    def delete(self, class_id):
        """Delete a class given its identifier."""
        delete_class(class_id)
        return None, 204


@api.route("/level/<level_or_me>")
@api.response(404, "Level not found")
class ClassLevelResource(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_list_with(class_model)
    def get(self, level_or_me):
        """Fetch all classes for a given level."""
        try:
            if level_or_me == "me":
                user_level = current_user.level
            else:
                user_level = UserLevel(level_or_me)
            classes = get_classes_from_level(user_level)
            if not classes:
                api.abort(404, f"No classes found for level {level_or_me}")
            return classes
        except ValueError:  # If "level" is not a valid UserLevel
            api.abort(404, f"Invalid level {level_or_me}")
            
@api.route("/teacherclasses/<teacher_id_or_me>")
@api.response(404, "Teacher id not found")
class ClassTeacherResource(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_list_with(class_model)
    def get(self, teacher_id_or_me):
        """Fetch all classes for a given teacher_id."""
        try:
            if teacher_id_or_me == "me":
                user_id = current_user.user_id
            classes = get_classes_from_teacher(user_id)
            if not classes:
                api.abort(404, f"No classes found for teacher_id {user_id}")
            return classes
        except ValueError:  # If "teacher_id" is not a valid teacher_id
            api.abort(404, f"Invalid level teacher_id {user_id}")


@api.route("/<int:class_id>/messages")
class ClassMessages(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_list_with(message_model)
    def get(self, class_id):
        """Get all messages for the main group of a specific class."""
        class_ = get_class_by_id(class_id)
        if not class_:
            api.abort(404, f"Class with id {class_id} not found")
        return [message.as_dict() for message in get_class_messages(class_)]

    @api.doc(security="apikey")
    @require_authentication()
    @api.expect(message_post_model)
    def post(self, class_id):
        """Post a new message to the main group of a specific class."""
        content = api.payload.get("content")
        message = add_class_message(content, class_id=class_id, user_id=current_user.user_id)
        if message:
            return api.marshal(message.as_dict(), message_model), 201
        api.abort(400, "Could not add message to the class")


@api.route("/<int:class_id>/homework")
class GroupHomework(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_list_with(homework_model)
    def get(self, class_id):
        """Get all homework for a specific class group."""
        return [hmw.as_dict() for hmw in get_class_homework(class_id)]

    @api.doc(security="apikey")
    @require_authentication("admin", "teacher")
    @api.expect(homework_post_model)
    def post(self, class_id):
        """Post a new homework to a specific class group."""
        content = api.payload.get("content")
        due_date = api.payload.get("due_date")
        due_time = api.payload.get("due_time")
        hmw = add_homework_to_class(content, class_id=class_id, due_date=due_date, due_time=due_time)
        if hmw:
            return api.marshal(hmw.as_dict(), homework_model), 201
        api.abort(400, "Could not add homework to the class")
