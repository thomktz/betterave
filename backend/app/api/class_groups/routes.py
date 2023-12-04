from flask_restx import Resource
from flask_login import current_user
from .models import class_group_model, message_model, message_post_model
from .namespace import api
from app.operations.class_group_operations import (
    get_all_class_groups,
    add_class_group,
    get_class_group_by_id,
    update_class_group,
    delete_class_group
)
from app.operations.message_operations import (
    get_messages_by_group_id,
    add_message_to_group,
    delete_message
)
from app.decorators import require_authentication

@api.route("/")
class ClassGroupList(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_list_with(class_group_model)
    def get(self):
        """List all class groups"""
        return get_all_class_groups()

    @api.doc(security="apikey")
    @require_authentication("admin", "teacher")
    @api.expect(class_group_model)
    def post(self):
        """Create a new class group"""
        return add_class_group(api.payload), 201

@api.route("/<int:group_id>")
@api.response(404, "Class group not found")
class ClassGroupResource(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_with(class_group_model)
    def get(self, group_id):
        """Fetch a class group given its identifier"""
        group = get_class_group_by_id(group_id)
        if group:
            return group
        api.abort(404, "Class group not found")

    @api.doc(security="apikey")
    @require_authentication("admin", "teacher")
    @api.expect(class_group_model)
    @api.response(204, "Class group successfully updated")
    def put(self, group_id):
        """Update a class group given its identifier"""
        if update_class_group(group_id, api.payload):
            return None, 204
        api.abort(400, "Could not update class group.")

    @api.doc(security="apikey")
    @require_authentication("admin", "teacher")
    @api.response(204, "Class group successfully deleted")
    def delete(self, group_id):
        """Delete a class group given its identifier"""
        if delete_class_group(group_id):
            return None, 204
        api.abort(404, "Class group not found or could not be deleted")

@api.route("/<int:group_id>/messages")
class GroupMessages(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_list_with(message_model)
    def get(self, group_id):
        """Get all messages for a specific class group"""
        return [message.as_dict() for message in get_messages_by_group_id(group_id)]

    @api.doc(security="apikey")
    @require_authentication()
    @api.expect(message_post_model)
    def post(self, group_id):
        """Post a new message to a specific class group"""
        content = api.payload.get("content")
        message = add_message_to_group(content, user_id=current_user.user_id, group_id=group_id)
        if message:
            return api.marshal(message.as_dict(), message_model), 201
        api.abort(400, "Could not add message to the class")
        

@api.route("/messages/<int:message_id>")
@api.response(404, "Message not found")
class MessageResource(Resource):
    @api.doc(security="apikey")
    @require_authentication("admin", "teacher")
    @api.response(204, "Message successfully deleted")
    def delete(self, message_id):
        """Delete a specific message"""
        if delete_message(message_id):
            return None, 204
        api.abort(404, "Message not found")