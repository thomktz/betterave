import pytest
from app.models.user import User
from app.models import UserType, UserLevel
from datetime import date, time, datetime
from app.operations.class_operations import add_class
from app.operations.class_group_operations import add_class_group, delete_class_group
from app.operations.lesson_operations import (
    add_lesson,
    update_lesson,
    delete_lesson,
    get_lesson_by_id,
    get_all_lessons,
    get_all_future_lessons,
    get_lessons_by_class,
    get_student_lessons,
    get_student_future_lessons,
    get_teacher_lessons,
    get_teacher_future_lessons
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
STUDENT_NAME = ("Lucas", "Dough")
HOMEWORK = "Solve problem set 4"
ROOM = "A1"


@pytest.fixture
def setup_teacher(test_client):
    """Create a user and returns their ID."""
    student_id = add_user("John", "Adams", "teacher_pic_url", UserType.TEACHER, UserLevel.NA)
    return student_id


@pytest.fixture
def setup_student(test_client):
    """Create a user and returns their ID."""
    student_id = add_user(STUDENT_NAME[0], STUDENT_NAME[1], "student_pic_url", UserType.STUDENT, UserLevel._1A)
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


def test_get_lesson_by_id(test_client, setup_lesson):
    """Test getting a lesson by its ID."""
    lesson = get_lesson_by_id(setup_lesson)
    assert lesson is not None
    assert lesson.lesson_id == setup_lesson


def test_get_all_lessons(test_client, setup_lesson):
    """Test getting all lessons."""
    lessons = get_all_lessons()
    assert lessons is not None
    assert len(lessons) >= 1


def test_get_all_future_lessons(test_client, setup_lesson):
    """Test getting all future lessons."""
    future_lessons = get_all_future_lessons()
    assert future_lessons is not None
    assert all(lesson.date >= datetime.now().date() for lesson in future_lessons)


def test_get_lesson_by_id(test_client, setup_lesson):
    """Test getting a lesson by its ID."""
    lesson = get_lesson_by_id(setup_lesson)
    assert lesson is not None
    assert lesson.lesson_id == setup_lesson


def test_get_all_lessons(test_client, setup_lesson):
    """Test getting all lessons."""
    lessons = get_all_lessons()
    assert lessons is not None
    assert len(lessons) >= 1


def test_get_all_future_lessons(test_client, setup_lesson):
    """Test getting all future lessons."""
    future_lessons = get_all_future_lessons()
    assert future_lessons is not None
    assert all(lesson.date >= datetime.now().date() for lesson in future_lessons)


def test_get_lessons_by_class(test_client, setup_lesson, setup_class):
    """Test getting lessons for a particular class."""
    class_lessons = get_lessons_by_class(setup_class)
    assert class_lessons is not None
    assert all(lesson.group.class_id == setup_class for lesson in class_lessons)


def test_get_student_lessons(test_client, setup_lesson, setup_student):
    """Test getting lessons for a student."""
    student_lessons = get_student_lessons(User.query.get(setup_student))
    assert student_lessons is not None
    assert len(student_lessons) >= 1


def test_get_student_future_lessons(test_client, setup_lesson, setup_student):
    """Test getting future lessons for a student."""
    student_future_lessons = get_student_future_lessons(User.query.get(setup_student))
    assert student_future_lessons is not None
    assert all(lesson.date >= datetime.now().date() for lesson in student_future_lessons)


def test_get_teacher_lessons(test_client, setup_lesson, setup_teacher):
    """Test getting lessons for a teacher."""
    teacher_lessons = get_teacher_lessons(User.query.get(setup_teacher))
    assert teacher_lessons is not None
    assert len(teacher_lessons) >= 1


def test_get_teacher_future_lessons(test_client, setup_lesson, setup_teacher):
    """Test getting future lessons for a teacher."""
    teacher_future_lessons = get_teacher_future_lessons(User.query.get(setup_teacher))
    assert teacher_future_lessons is not None
    assert all(lesson.date >= datetime.now().date() for lesson in teacher_future_lessons)
