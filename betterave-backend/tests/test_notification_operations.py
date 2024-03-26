import pytest
from betterave_backend.app.models import User, UserType, UserLevel
from datetime import date, time
from betterave_backend.app.operations.notification_operations import (
    add_notification,
    update_notification,
    delete_notification,
    get_notification_by_id,
    get_all_notifications,
    get_user_notifications,
    add_recipient_to_notification,
)
from betterave_backend.app.operations.user_operations import add_user

# Constants
TITLE = "New Notification"
CONTENT = "This is a test notification content"
SENT_BY_USER_ID = 1
RECIPIENT_TYPE = "All users"

@pytest.fixture
def setup_user(test_client):
    """Create a user and returns their ID."""
    user_id = add_user("John", "Doe", "user_pic_url", UserType.ADMIN, UserLevel.NA)
    return user_id

@pytest.fixture
def setup_notification(test_client):
    """Fixture to create a notification and return its ID."""
    event_id = add_notification(
            title=TITLE,
            content=CONTENT,
            sent_by_user_id = SENT_BY_USER_ID ,
            recipient_type=RECIPIENT_TYPE,
            )
    yield event_id
    delete_notification(event_id)
    
@pytest.fixture
def setup_student(test_client):
    """Create a student user and returns their ID."""
    student_id = add_user("John", "Mac", "student_pic_url", UserType.STUDENT, UserLevel._1A)
    return student_id



def test_add_notification(test_client):
    """Test adding a new notification."""
    notification_id = add_notification(
        title=TITLE,
        content=CONTENT,
        sent_by_user_id=SENT_BY_USER_ID,
        recipient_type=RECIPIENT_TYPE,
    )
    assert notification_id is not None
    assert notification_id > 0

def test_update_notification(test_client, setup_notification):
    """Test modifying a notification."""
    new_content = "Updated notification content"
    success = update_notification(setup_notification, {"content": new_content})
    assert success is True
    modified_notification = get_notification_by_id(setup_notification)
    assert modified_notification.content == new_content

def test_delete_notification(test_client, setup_notification):
    """Test removing a notification."""
    success = delete_notification(setup_notification)
    assert success is True
    assert get_notification_by_id(setup_notification) is None

def test_get_notification_by_id(test_client, setup_notification):
    """Test getting a notification by ID."""
    notification = get_notification_by_id(setup_notification)
    assert notification is not None
    assert notification.notification_id == setup_notification

def test_get_all_notifications(test_client):
    """Test getting all notifications."""
    notifications = get_all_notifications()
    assert len(notifications) >= 1

def test_get_user_notifications(test_client, setup_user):
    """Test getting notifications received by a user."""
    user_notifications = get_user_notifications(User.query.get(setup_user))
    assert len(user_notifications) >= 1

def test_add_recipient_to_notification(test_client, setup_notification):
    """Test adding recipients to a notification."""
    success = add_recipient_to_notification(setup_notification, user_ids=[setup_student])
    assert success is True
