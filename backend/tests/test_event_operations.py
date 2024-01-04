import pytest
from app.models.user import User
from app.models import UserType, UserLevel
from datetime import date, time
from app.operations.class_operations import add_class
from app.operations.class_group_operations import add_class_group, delete_class_group
from app.operations.event_operations import (
    add_event,
    update_event,
    delete_event,
    get_event_by_id,
    get_all_events,
    get_association_events,
    get_user_events,
    get_all_future_events,
    get_user_future_events,
    get_association_future_events,
    add_attendees_to_event,
    can_create_event
)
from app.operations.user_operations import add_user

# Constants
ASSO_ID = 101
ASSO_NAME = "Test Event"
EVENT_DATE = date(2024,10,20)
START_TIME = time(9,0,0)
END_TIME = time(10,0,0)
DESCRIPTION = "Test Réunion"
LOCATION = "Amphi 200"
PARTICIPANT_TYPE = "All users"


@pytest.fixture
def setup_student(test_client):
    """Create a student user and returns their ID."""
    student_id = add_user("John", "Mac", "student_pic_url", UserType.STUDENT, UserLevel._1A)
    return student_id

@pytest.fixture
def setup_event(test_client,):
    """Fixture to create an event and return its ID."""
    event_id = add_event(
        asso_id=ASSO_ID,
        asso_name=ASSO_NAME,
        start_time=START_TIME,
        end_time=END_TIME,
        participants=PARTICIPANT_TYPE,
        description=DESCRIPTION,
        location=LOCATION
    )
    yield event_id
    delete_event(event_id)


def test_add_event(test_client,):
    """Test adding a new lesson."""
    event_id = add_event(
        asso_id=ASSO_ID,
        asso_name=ASSO_NAME,
        start_time=START_TIME,
        end_time=END_TIME,
        participants=PARTICIPANT_TYPE,
        description=DESCRIPTION,
        location=LOCATION
    )
    assert event_id is not None
    assert event_id > 0

def test_update_event(test_client, setup_event):
    """Test modifying an event."""
    new_description = "Conférence sur le climat"
    success = update_event(setup_event,{"description": new_description})
    assert success is True
    modified_event = get_event_by_id(setup_event)
    assert modified_event.description == new_description


def test_delete_lesson(test_client, setup_event):
    """Test removin an event."""
    success = delete_event(setup_event)
    assert success is True
    assert get_event_by_id(setup_student) is None


def test_get_event_by_id(test_client, setup_event):
    """Test getting an event by ID."""
    event = get_event_by_id(setup_event)
    assert event is not None
    assert event.event_id == setup_event


def test_get_all_events(test_client, setup_event):
    """Test getting all events."""
    events = get_all_events()
    assert len(events) >= 1


def test_get_association_events(test_client, setup_event):
    """Test getting events organized by a particular association."""
    asso_user_id = 31 # Tribu ENSAE
    asso_events = get_association_events(User.query.get(asso_user_id))
    assert len(asso_events) >= 1


def test_get_user_events(test_client, setup_event, setup_student):
    """Test getting events attended by a particular user."""
    user_events = get_user_events(User.query.get(setup_student))
    assert len(user_events) >= 1


def test_get_all_future_events(test_client, setup_event):
    """Test getting all future events."""
    future_events = get_all_future_events()
    assert len(future_events) >= 1


def test_get_association_future_events(test_client, setup_event):
    """Test getting future events organized by a particular association."""
    asso_user_id = 31  # Tribu ENSAE
    future_asso_events = get_association_future_events(User.query.get(asso_user_id))
    assert len(future_asso_events) >= 1


def test_get_user_future_events(test_client, setup_event, setup_student):
    """Test getting future events attended by a particular user."""
    future_user_events = get_user_future_events(User.query.get(setup_student))
    assert len(future_user_events) >= 1


def test_add_attendees_to_event(test_client, setup_event, setup_student):
    """Test adding attendees to an event."""
    success = add_attendees_to_event(setup_event, user_ids=[setup_student])
    assert success is True
    updated_event = get_event_by_id(setup_event)
    assert setup_student in updated_event.attending_users


def test_can_create_event(test_client, setup_student):
    """Test checking if a user can create an event."""
    user_can_create = can_create_event(User.query.get(setup_student))
    assert user_can_create is True


