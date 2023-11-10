from flask_restx import fields
from .namespace import api

class AssoNameModel(fields.Raw):
    def format(self, value):
        return value.name

class EventBackgroundColorModel(fields.Raw):
    def format(self, value):
        # Return a default color for events
        return '#FFFFFF'

fullcalendar_event_model = api.model('Event', {
    "id": fields.String(
        attribute=lambda x: f"event_{x.event_id}",
        description="A unique identifier for the event prefixed with 'event_'"
    ),
    "resourceId": fields.Integer(
        attribute=lambda x: x.association_id,
        description="The identifier of the association that is hosting the event, used for associating events with resources"
    ),
    "start": fields.DateTime(
        dt_format='iso8601', 
        attribute=lambda x: datetime.combine(x.date, x.start_time).isoformat(),
        description="The start time of the event in ISO8601 format"
    ),
    "end": fields.DateTime(
        dt_format='iso8601', 
        attribute=lambda x: datetime.combine(x.date, x.end_time).isoformat(),
        description="The end time of the event in ISO8601 format"
    ),
    "title": fields.String(
        attribute=lambda x: x.association.name if x.association else "Unnamed Event",
        description="The name of the association or the main title of the event"
    ),
    "type": fields.String(
        attribute='description',
        description="A brief description or subtitle for the event"
    ),
    "backgroundColor": fields.String(
        attribute=lambda x: x.association.background_color if x.association and x.association.background_color else "#FFFFFF",
        description="The background color for the event, defaulting to white if not specified"
    ),
    "room": fields.String(
        attribute='location',
        description="The location where the event takes place"
    ),
    "event_id": fields.Integer(
        attribute='event_id',
        description="The internal unique identifier of the event"
    ),
    "lesson_id": fields.Integer(
        default=None,
        description="The unique identifier of the lesson, if applicable"
    ),
})


event_post_model = api.model('EventPost', {
    "asso_id": fields.Integer(required=True, description="The unique identifier of the association organizing the event"),
    "name": fields.String(required=True, description="The name of the event"),
    "date": fields.String(required=True, description="The date of the event in YYYY-MM-DD format"),
    "start_time": fields.String(required=True, description="The start time of the event in HH:MM:SS format"),
    "end_time": fields.String(required=True, description="The end time of the event in HH:MM:SS format"),
    "description": fields.String(description="A description of the event"),
    "location": fields.String(description="The location where the event will take place")
})

event_attendees_post_model = api.model('EventAttendeesPostModel', {
    'user_ids': fields.List(fields.Integer, description='List of user IDs to add to the event', required=False),
    'user_level': fields.String(description='User level to filter which users to add to the event', required=False),
    "asso_id": fields.Integer(description="The unique identifier of the association organizing the event", required=False),
})