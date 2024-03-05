# type: ignore
import pytest
from betterave_backend.app.models.class_ import Class
from betterave_backend.app.models.user import User
from betterave_backend.app.models import UserType, UserLevel
from betterave_backend.app.operations.class_operations import add_class
from betterave_backend.app.operations.class_group_operations import add_class_group
from betterave_backend.app.operations.homework_operations import (
    get_homework_by_group_id,
    add_homework_to_group,
    delete_homework,
    get_class_homework,
    add_homework_to_class,
    get_user_homework,
)
from betterave_backend.app.operations.user_operations import add_user

STUDENT_NAME = ("Alice", "Doe")
GROUP_NAME = "Test Group"
IS_MAIN_GROUP = True
DUE_DATE = "2023-12-31"
DUE_TIME = "23:59"
HOMEWORK_CONTENT = "Complete assignment 1"


@pytest.fixture
def setup_teacher(test_client):
    """Create a user and returns their ID."""
    student_id = add_user("Thomas", "Doe", "teacher_pic_url", UserType.TEACHER, UserLevel.NA)
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


def test_get_homework_by_group_id(test_client, setup_group):
    """Test retrieving homework for a specific class group."""
    homework_list = get_homework_by_group_id(setup_group)
    assert homework_list is not None


def test_add_homework_to_class(test_client, setup_class, setup_group):
    """Test adding homework to a specific class."""
    homework = add_homework_to_class(HOMEWORK_CONTENT, setup_class, DUE_DATE, DUE_TIME)
    assert homework is not None
    assert homework.content == HOMEWORK_CONTENT


def test_delete_homework(test_client, setup_group):
    """Test deleting homework."""
    homework = add_homework_to_group(HOMEWORK_CONTENT, DUE_DATE, DUE_TIME, setup_group)
    success = delete_homework(homework)
    assert success is True


def test_get_class_homework(test_client, setup_class, setup_group):
    """Test retrieving homework for a specific class."""
    class_homework = get_class_homework(Class.query.get(setup_class))
    assert class_homework is not None
    assert isinstance(class_homework, list)


def test_get_user_homework(test_client, setup_student):
    """Test retrieving homework for a specific user."""
    user_homework = get_user_homework(User.query.get(setup_student))
    assert user_homework is not None
    assert isinstance(user_homework, list)
