from flask_restx import Resource
from .namespace import api
from .models import (
    fullcalendar_event_model,
    event_post_model,
    event_attendees_post_model,
)
from app.operations.event_operations import (
    add_event,
    add_attendees_to_event,
    can_create_event,
    get_all_events,
    delete_event,
    get_event_by_id,
)
from app.decorators import require_authentication
from flask_login import current_user


@api.route("/")
class EventList(Resource):
    @api.doc(security="apikey")
    @require_authentication()
    @api.marshal_list_with(fullcalendar_event_model)
    def get(self):
        """Get a list of all events."""
        return get_all_events()

    @api.doc(security="apikey")
    @require_authentication()
    @api.expect(event_post_model)
    @api.marshal_with(fullcalendar_event_model)
    def post(self):
        """Create a new event."""
        event_data = api.payload
        if can_create_event(current_user, event_data["asso_id"]):
            event_id = add_event(**event_data)
            event = get_event_by_id(event_id)
            if event:
                return event, 201
            else:
                api.abort(400, "Could not create the event")
        api.abort(403, "Permission denied")


@api.route("/<int:event_id>")
class EventResource(Resource):
    @api.doc(security="apikey")
    @require_authentication("admin", "asso")
    def delete(self, event_id):
        """Delete an event."""
        if delete_event(event_id):
            return {"message": "Event deleted successfully"}, 200
        api.abort(400, "Could not delete the event")


@api.route("/<int:event_id>/attendees")
class EventAttendees(Resource):
    @api.doc(security="apikey")
    @require_authentication("admin", "asso")
    @api.expect(event_attendees_post_model)
    def post(self, event_id):
        """Add attendees to an event."""
        user_ids = api.payload.get("user_ids", [])
        user_level = api.payload.get("user_level", None)
        asso_id = api.payload.get("asso_id", None)
        if add_attendees_to_event(event_id, user_ids, user_level, asso_id):
            return {"message": "Attendees added successfully"}, 200
        api.abort(400, "Could not add attendees to the event")
