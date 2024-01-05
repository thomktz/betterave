# type: ignore
from flask_restx import Resource
from .models import user_class_group_model, user_class_group_update_model
from .namespace import api
from app.operations.user_class_group_operations import (
    add_user_class_group,
    get_user_class_group_by_id,
    update_user_class_group,
    delete_user_class_group,
    get_ucg_by_user_and_class,
)
from app.operations.class_group_operations import get_class_group_by_name
from app.decorators import require_authentication


@api.route("/")
class UserClassGroupList(Resource):
    @api.doc(security="apikey")
    @require_authentication("admin")
    @api.expect(user_class_group_model)
    def post(self):
        """Create a new user-class group relationship."""
        return add_user_class_group(api.payload), 201


@api.route("/<int:id>")
@api.response(404, "User-Class Group relationship not found")
class UserClassGroupResource(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_with(user_class_group_model)
    def get(self, id):
        """Fetch a user-class group relationship given its identifier."""
        user_class_group = get_user_class_group_by_id(id)
        if user_class_group:
            return user_class_group
        api.abort(404, "User-Class Group relationship not found")

    @api.doc(security="apikey")
    @require_authentication("admin")
    @api.response(204, "User-Class Group relationship successfully deleted")
    def delete(self, id):
        """Delete a user-class group relationship given its identifier."""
        if delete_user_class_group(id):
            return None, 204
        api.abort(404, "User-Class Group relationship not found or could not be deleted")


@api.route("/<int:user_id>/<int:class_id>")
@api.response(404, "User-Class Group relationship not found")
class UserClassGroupDetail(Resource):
    @api.doc(security="apikey")
    @require_authentication("admin")
    @api.expect(user_class_group_update_model)
    @api.response(200, "User-Class Group relationship successfully updated")
    @api.response(204, "No changes were made to the User-Class Group relationship")
    def put(self, user_id, class_id):
        """Update the secondary class group associated with the user-class group relationship."""
        data = api.payload
        secondary_class_group_name = data.get("secondary_class_group_name")

        # Logic to update the user-class group relationship
        secondary_class_group = get_class_group_by_name(class_id, secondary_class_group_name)
        if not secondary_class_group:
            api.abort(404, "Secondary class group not found")

        user_class_group = get_ucg_by_user_and_class(user_id, class_id)
        if not user_class_group:
            api.abort(404, "User-Class Group relationship not found")

        # Check if there is actually an update to the secondary class group
        if user_class_group.secondary_class_group_id == secondary_class_group.group_id:
            return {"message": "No changes were made to the User-Class Group relationship"}, 204

        # Perform the update
        success = update_user_class_group(
            user_class_group,
            {"secondary_class_group_id": secondary_class_group.group_id},
        )
        if success:
            updated_user_class_group = get_user_class_group_by_id(user_class_group.id)
            return api.marshal(updated_user_class_group, user_class_group_model), 200
        else:
            api.abort(400, "Failed to update User-Class Group relationship")
