from datetime import datetime
from flask_restx import fields
from .namespace import api


class AssoNameModel(fields.Raw):
    def format(self, value):
        """Format the association name to be displayed in the calendar."""
        return value.name


class NotificationBackgroundColorModel(fields.Raw):
    def format(self, value):
        """Define the default background color for notifications."""
        return "#FFFFFF"



notification_post_model = api.model(
    "NotificationPost",
    {
        "sent_by_user_id": fields.Integer(
            required=True,
            description="The unique identifier of the user sending the notification",
        ),
        "title": fields.String(required=True, description="The name of the notification"),
        "content": fields.String(description="A description of the notification"),
        "recipient_type": fields.String(
            required=True,
            description="Users that will receive the notification. ['Subscribers', 'All users'] or a UserLevel.",
        ),
    },
)

notification_recipients_post_model = api.model(
    "notificationRecipientsPostModel",
    {
        "user_ids": fields.List(
            fields.Integer,
            description="List of user IDs to receive the notification",
            required=False,
        ),
        "user_level": fields.String(
            description="User level to filter which users will receive the notification",
            required=False,
        ),
        "sender_id": fields.Integer(
            description="The unique identifier of the user (asso or admin) sending the notification",
            required=False,
        ),
    },
)
