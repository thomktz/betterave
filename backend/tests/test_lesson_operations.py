import pytest
from app.models import UserType, UserLevel
from datetime import date, time
from app.operations.class_operations import add_class
from app.operations.class_group_operations import add_class_group, delete_class_group
from app.operations.lesson_operations import (
    add_lesson,
    update_lesson,
    delete_lesson,
    get_lesson_by_id,
)
from app.operations.user_operations import add_user

# Constants
CLASS_NAME = "Test Class"
CLASS_ID = 101
ECTS_CREDITS = 3
LEVEL = "1A"
BACKGROUND_COLOR = "#123456"
GROUP_NAME = "Test Group"
IS_MAIN_GROUP = True
LESSON_DATE = date(2023, 10, 21)
START_TIME = time(9, 0, 0)
END_TIME = time(10, 0, 0)
STUDENT_NAME = ("Alice", "Smith")
HOMEWORK = "Solve problem set 4"
ROOM = "A1"


@pytest.fixture
def setup_teacher(test_client):
    """Creates a user and returns their ID."""
    student_id = add_user("John", "Doe", "teacher_pic_url", UserType.TEACHER, UserLevel.NA)
    return student_id


@pytest.fixture
def setup_class(test_client, setup_teacher):
    """Fixture to create a class and return its instance."""
    class_id = add_class(
        class_id=CLASS_ID,
        name=CLASS_NAME,
        ects_credits=ECTS_CREDITS,
        default_teacher_id=setup_teacher,
        level=LEVEL,
        background_color=BACKGROUND_COLOR,
    )
    return class_id


@pytest.fixture
def setup_group(test_client, setup_class):
    """Fixture to create a class group within the setup class and return its ID."""
    group_id = add_class_group(name=GROUP_NAME, class_id=setup_class, is_main_group=IS_MAIN_GROUP)
    yield group_id
    delete_class_group(group_id)


@pytest.fixture
def setup_lesson(test_client, setup_group, setup_teacher):
    """Fixture to create a lesson and return its ID."""
    lesson_id = add_lesson(
        group_id=setup_group,
        date=LESSON_DATE,
        start_time=START_TIME,
        end_time=END_TIME,
        homework=HOMEWORK,
        room=ROOM,
        teacher_id=setup_teacher,
    )
    yield lesson_id
    delete_lesson(lesson_id)


def test_add_lesson(test_client, setup_group, setup_teacher):
    """Test adding a new lesson."""
    lesson_id = add_lesson(
        group_id=setup_group,
        date=LESSON_DATE,
        start_time=START_TIME,
        end_time=END_TIME,
        homework=HOMEWORK,
        room=ROOM,
        teacher_id=setup_teacher,
    )
    assert lesson_id is not None
    assert lesson_id > 0


def test_update_lesson(test_client, setup_lesson):
    """Test modifying a lesson."""
    new_homework = "Solve problem set 5"
    success = update_lesson(setup_lesson, {"homework": new_homework})
    assert success is True
    modified_lesson = get_lesson_by_id(setup_lesson)
    assert modified_lesson.homework == new_homework


def test_delete_lesson(test_client, setup_lesson):
    """Test removing a lesson."""
    success = delete_lesson(setup_lesson)
    assert success is True
    assert get_lesson_by_id(setup_lesson) is None
