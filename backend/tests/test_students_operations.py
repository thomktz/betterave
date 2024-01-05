import pytest
from app.models.class_group import ClassGroup
from app.models.user import User
from app.models.class_ import Class
from app.models import UserType, UserLevel
from app.operations.class_operations import add_class
from app.operations.class_group_operations import add_class_group, delete_class_group, enroll_student_in_group
from app.operations.student_operations import (
    get_all_students,
    get_student_groups,
    get_students_from_class,
    get_students_from_level,
    is_student_in_class,
    is_student_in_group
)
from app.operations.user_operations import add_user

# Constants
STUDENT_NAME = ("Alice", "Smith")


@pytest.fixture
def setup_student(test_client):
    """Create a user and returns their ID."""
    student_id = add_user(STUDENT_NAME[0], STUDENT_NAME[1], "student_pic_url", UserType.STUDENT, UserLevel._1A)
    return student_id


@pytest.fixture
def setup_teacher(test_client):
    """Create a user and returns their ID."""
    student_id = add_user("John", "Doe", "teacher_pic_url", UserType.TEACHER, UserLevel.NA)
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
def setup_group(test_client, setup_class):
    """Fixture to create a class group within the setup class and return its ID."""
    group_id = add_class_group(name="Test Group", class_id=setup_class, is_main_group=True)
    yield group_id
    delete_class_group(group_id)


def test_get_student_groups(test_client, setup_student, setup_group, setup_class):
    """Test getting class groups a student is enrolled in."""
    enroll_student_in_group(setup_student, setup_group)
    student_groups = get_student_groups(User.query.get(setup_student))
    assert len(student_groups) >= 1
    assert setup_group in student_groups


def test_get_all_students(test_client, setup_student):
    """Test getting all student users."""
    all_students = get_all_students()
    assert len(all_students) >= 1
    assert User.query.get(setup_student) in all_students


def test_get_students_from_level(test_client, setup_student):
    """Test getting students from a specific level."""
    students_from_level = get_students_from_level(UserLevel._1A)
    assert len(students_from_level) >= 1
    assert User.query.get(setup_student) in students_from_level


def test_is_student_in_group(test_client, setup_student, setup_group):
    """Test checking if a student is in a specific class group."""
    enroll_student_in_group(setup_student, setup_group)
    result = is_student_in_group(User.query.get(setup_student), ClassGroup.query.get(setup_group))
    assert result is True


def test_is_student_in_class(test_client, setup_student, setup_class):
    """Test checking if a student is in the main group of a specific class."""
    result = is_student_in_class(User.query.get(setup_student), Class.query.get(setup_class))
    assert result is True


def test_get_students_from_class(test_client, setup_student, setup_class):
    """Test getting students who have taken a specific class."""
    students_from_class = get_students_from_class(setup_class)
    assert len(students_from_class) >= 1
    assert User.query.get(setup_student) in students_from_class