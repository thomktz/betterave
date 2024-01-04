# type: ignore
import pytest
from app.operations.class_group_operations import (
    add_class_group,
    delete_class_group,
    update_class_group,
    get_class_group_by_id,
    enroll_student_in_group,
    unenroll_student_from_group,
)
from app.operations.user_operations import add_user, delete_user
from app.operations.class_operations import add_class
from app.models import UserType, UserLevel

# Constants for the test
GROUP_NAME = "Test Group"
IS_MAIN_GROUP = True
CLASS_ID = 0
CLASS_NAME = "Test Class"
LEVEL = "1A"
ECTS_CREDITS = 3  # example attribute for a class
BACKGROUND_COLOR = "#123456"


@pytest.fixture
def setup_teacher(test_client):
    """Create a user and returns their ID."""
    teacher_id = add_user("John", "Doe", "teacher_pic_url", UserType.TEACHER, UserLevel.NA)
    return teacher_id


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
def setup_student(test_client):
    """Fixture to create a student and return their ID."""
    student_id = add_user("Jane", "Doe", "student_pic_url", UserType.STUDENT, UserLevel._1A)
    yield student_id
    delete_user(student_id)


def test_add_class_group(setup_class):
    """Test adding a new class group."""
    group_id = add_class_group(name=GROUP_NAME, class_id=setup_class, is_main_group=IS_MAIN_GROUP)
    assert group_id != -1


def test_update_class_group(setup_group):
    """Test modifying a class group."""
    NEW_NAME = "Updated Group Name"
    assert update_class_group(setup_group, {"name": NEW_NAME}) is True
    group = get_class_group_by_id(setup_group)
    assert group.name == NEW_NAME  # Check that the group name was updated.


def test_delete_class_group(setup_group):
    """Test deleting a class group."""
    assert delete_class_group(setup_group) is True
    group = get_class_group_by_id(setup_group)
    assert group is None  # Check that the group was deleted.


def test_enroll_student_in_group(setup_student, setup_group):
    """Test enrolling a student in a group."""
    assert enroll_student_in_group(setup_student, setup_group) is True
    group = get_class_group_by_id(setup_group)
    assert setup_student in [student.user_id for student in group.students]  # Check that the student was enrolled.


def test_unenroll_student_from_group(setup_student, setup_group):
    """Test unenrolling a student from a group."""
    # First, enroll the student
    enroll_student_in_group(setup_student, setup_group)
    # Now, test unenrolling
    assert unenroll_student_from_group(setup_student, setup_group) is True
    group = get_class_group_by_id(setup_group)
    assert setup_student not in [
        student.user_id for student in group.students
    ]  # Check that the student was unenrolled.
