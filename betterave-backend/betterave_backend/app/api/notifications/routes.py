from flask_restx import Resource
from .namespace import api
from .models import (
    notification_post_model,
    notification_recipients_post_model,
)
from betterave_backend.app.operations.notification_operations import (
    add_notification,
    add_recipient_to_notification,
    get_notification_by_id,
    get_all_notifications,
    delete_notification,
    get_notification_by_id,
    can_create_notification,
)
from betterave_backend.app.decorators import require_authentication
from flask_login import current_user


@api.route("/")
class NotificationList(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    def get(self):
        """Get a list of all notifications."""
        return get_all_notifications()

    @api.doc(security="apikey")
    @require_authentication()
    @api.expect(notification_post_model)
    def post(self):
        """Create a new notification."""
        notification_data = api.payload
        if can_create_notification(current_user, notification_data["asso_id"]):
            notification_id = add_notification(**notification_data)
            notification = get_notification_by_id(notification_id)
            if notification:
                return notification, 201
            else:
                api.abort(400, "Could not create the notification")
        api.abort(403, "Permission denied")


@api.route("/<int:notification_id>")
class NotificationResource(Resource):
    @api.doc(security="apikey")
    @require_authentication("admin", "asso")
    def delete(self, notification_id):
        """Delete an notification."""
        if delete_notification(notification_id):
            return {"message": "Notification deleted successfully"}, 200
        api.abort(400, "Could not delete the notification")


@api.route("/<int:notification_id>/recipients")
class NotificationRecipients(Resource):
    @api.doc(security="apikey")
    @require_authentication("admin", "asso")
    @api.expect(notification_recipients_post_model)
    def post(self, notification_id):
        """Link recipients to a notification."""
        user_ids = api.payload.get("user_ids", [])
        user_level = api.payload.get("user_level", None)
        asso_id = api.payload.get("asso_id", None)
        if add_recipient_to_notification(notification_id, user_ids, user_level, asso_id):
            return {"message": "Recipients added successfully"}, 200
        api.abort(400, "Could not add recipients to the notification")
