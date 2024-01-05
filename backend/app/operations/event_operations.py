# type: ignore
from typing import Optional
from datetime import datetime
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from app.models import Event, User, UserLevel
from app.decorators import is_valid_apikey, with_instance


def add_event(
    asso_id: int,
    name: str,
    date: str,
    start_time: str,
    end_time: str,
    participants: str,
    description: str = None,
    location: str = None,
) -> int:
    """Add an event to the database."""
    try:
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%H:%M").time()
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%H:%M").time()

        if participants == "Subscribers":
            attending_users = User.query.get(asso_id).subscribers
        elif participants == "All users":
            attending_users = User.query.all()
        else:
            # Participants is a UserLevel
            attending_users = User.query.filter_by(level=UserLevel(participants)).all()

        new_event = Event(
            asso_id=asso_id,
            name=name,
            date=date,
            start_time=start_time,
            end_time=end_time,
            description=description,
            location=location,
            attending_users=attending_users,
            participant_type=participants,
        )
        db.session.add(new_event)
        db.session.commit()
        return new_event.event_id
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error adding event: {str(e)}")
        return -1


def update_event(event_id: int, new_data: dict) -> bool:
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


@with_instance(User)
def get_association_events(asso: User, limit: Optional[int] = None) -> list[Event]:
    """Get all events organized by a particular association."""
    events = (
        Event.query.filter_by(asso_id=asso.user_id).limit(limit).all()
        if limit is not None
        else Event.query.filter_by(asso_id=asso.user_id).all()
    )
    return events


@with_instance(User)
def get_user_events(user: User, limit: Optional[int] = None) -> list[Event]:
    """Get all events a particular user is attending."""
    if limit is not None:
        event = user.attended_events[:limit]
    else:
        event = user.attended_events

    return event


def get_all_future_events() -> list[Event]:
    """Get all future events."""
    return Event.query.filter(Event.date >= datetime.now().date()).all()


@with_instance(User)
def get_association_future_events(asso: User, limit: Optional[int] = None) -> list[Event]:
    """Get all future events organized by a particular association."""
    if limit is not None:
        future_events = (
            Event.query.filter_by(asso_id=asso.user_id).filter(Event.date >= datetime.now().date()).limit(limit).all()
        )
    else:
        future_events = Event.query.filter_by(asso_id=asso.user_id).filter(Event.date >= datetime.now().date()).all()

    return future_events


@with_instance(User)
def get_user_future_events(user: User, limit: Optional[int] = None) -> list[Event]:
    """Get all future events a particular user is attending."""
    user_events = sorted([event for event in user.attended_events if event.date >= datetime.now().date()])
    return user_events[:limit] if limit is not None else user_events


def add_attendees_to_event(
    event_id: int, user_ids: Optional[int] = None, user_level: Optional[UserLevel] = None, asso_id: Optional[int] = None
) -> bool:
    """Add users to an event. If no users are specified, add all users."""
    event = Event.query.get(event_id)
    if not event:
        return False

    if user_ids:
        # Add specific users to the event
        users = User.query.filter(User.user_id.in_(user_ids)).all()
        event.attending_users.extend(users)
    elif user_level:
        # Add all users of a certain level to the event
        users = User.query.filter_by(level=user_level).all()
        event.attending_users.extend(users)
    elif asso_id:
        # Add all users subscribed to a particular association to the event
        asso = User.query.get(asso_id)
        if not asso:
            return False
        users = asso.subscribers
        event.attending_users.extend(users)
    else:
        # If no specific users or level provided, assume adding all users
        users = User.query.all()
        event.attending_users.extend(users)

    db.session.commit()
    return True


@with_instance(User)
def can_create_event(user: User, asso_id: Optional[int] = None) -> bool:
    """Check if a user can create an event."""
    # Assume that admin can create events for any association or for all users
    apikey = request.headers.get("X-API-KEY")
    if apikey and is_valid_apikey(apikey):
        return True
    if user.is_admin:
        return True
    # Associations can only create events for themselves
    if user.is_asso and (asso_id is None or user.user_id == asso_id):
        return True
    return False
