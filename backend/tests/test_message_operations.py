# type: ignore
import pytest
from backend.app.models.class_ import Class
from backend.app.models import UserType, UserLevel
from backend.app.operations.class_operations import add_class
from backend.app.operations.class_group_operations import add_class_group
from backend.app.operations.message_operations import (
    get_messages_by_group_id,
    add_message_to_group,
    delete_message,
    get_class_messages,
    add_class_message,
)
from backend.app.operations.user_operations import add_user

STUDENT_NAME = ("Zoe", "Smith")
GROUP_NAME = "Test Group"
IS_MAIN_GROUP = True
MESSAGE_CONTENT = "Hello, this is a test message!"


@pytest.fixture
def setup_teacher(test_client):
    """Create a user and returns their ID."""
    student_id = add_user("Allan", "Doe", "teacher_pic_url", UserType.TEACHER, UserLevel.NA)
    return student_id


@pytest.fixture
def setup_class(test_client, setup_teacher):
    """Fixture to create a class and return its instance."""
    class_id = add_class(
        class_id=101,
        name="Test Class",
        ects_credits=3,
        default_teacher_id=setup_teacher,
        level=UserLevel._1A,
        background_color="#123456",
    )
    return class_id


@pytest.fixture
def setup_student(test_client):
    """Create a user and returns their ID."""
    student_id = add_user(STUDENT_NAME[0], STUDENT_NAME[1], "student_pic_url", UserType.STUDENT, UserLevel._1A)
    return student_id


@pytest.fixture
def setup_group(test_client, setup_class):
    """Fixture to create a class group within the setup class and return its ID."""
    group_id = add_class_group(name=GROUP_NAME, class_id=setup_class, is_main_group=IS_MAIN_GROUP)
    return group_id


def test_get_messages_by_group_id(test_client, setup_group):
    """Test retrieving messages for a specific class group."""
    messages = get_messages_by_group_id(setup_group)
    assert messages is not None


def test_add_message_to_group(test_client, setup_group, setup_student):
    """Test adding a message to a specific class group."""
    message = add_message_to_group(MESSAGE_CONTENT, setup_group, setup_student)
    assert message is not None
    assert message.content == MESSAGE_CONTENT


def test_delete_message(test_client, setup_group, setup_student):
    """Test deleting a message."""
    message = add_message_to_group(MESSAGE_CONTENT, setup_group, setup_student)
    success = delete_message(message)
    assert success is True


def test_get_class_messages(test_client, setup_class, setup_group):
    """Test retrieving messages for a specific class."""
    class_messages = get_class_messages(Class.query.get(setup_class))
    assert class_messages is not None


def test_add_class_message(test_client, setup_class, setup_student, setup_group):
    """Test adding a message to a specific class's main group."""
    class_message = add_class_message(MESSAGE_CONTENT, setup_class, setup_student)
    assert class_message is not None
    assert class_message.content == MESSAGE_CONTENT
