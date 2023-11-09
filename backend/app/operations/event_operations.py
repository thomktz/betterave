from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from app.models import Event
from app.operations.user_operations import get_user_by_id

def add_event(asso_id, name, date, start_time, end_time, description=None, location=None):
    """Add an event to the database."""
    try:
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M:%S").time()
        
        new_event = Event(
            asso_id=asso_id,
            name=name,
            date=date,
            start_time=start_time,
            end_time=end_time,
            description=description,
            location=location
        )
        db.session.add(new_event)
        db.session.commit()
        return new_event.event_id
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding event: {str(e)}")
        return -1

def update_event(event_id, new_data: dict) -> bool:
    """Modify event information in the database."""
    try:
        event = get_event_by_id(event_id)
        if event:
            for key, value in new_data.items():
                if hasattr(event, key):
                    setattr(event, key, value)
            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error modifying event: {str(e)}")
        return False

def delete_event(event_id: int) -> bool:
    """Remove an event from the database."""
    try:
        event = get_event_by_id(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error deleting event: {str(e)}")
        return False
    
def get_event_by_id(event_id: int) -> Event:
    """Get an event by its ID."""
    return db.session.get(Event, event_id)

def get_all_events() -> list[Event]:
    """Return all events in the database."""
    return Event.query.all()

def get_events_by_asso_id(asso_id: int) -> list[Event]:
    """Get all events organized by a particular association."""
    return Event.query.filter_by(asso_id=asso_id).all()

def get_events_by_attendee_id(user_id: int) -> list[Event]:
    """Get all events a particular user is attending."""
    user = get_user_by_id(user_id)
    return user.attended_events

def assign_attendees_to_event(event_id, attendees: list):
    """Assign a list of attendees to an event."""
    try:
        event = get_event_by_id(event_id)
        if event:
            event.attending_users.extend(attendees)
            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error assigning attendees to event: {str(e)}")
        return False

def add_attendee_to_event(event_id, attendee):
    """Assign a single attendee to an event."""
    try:
        event = get_event_by_id(event_id)
        if event:
            event.attending_users.append(attendee)
            db.session.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding attendee to event: {str(e)}")
        return False
