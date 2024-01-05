import pytest
from app.models import UserType, UserLevel
from app.operations.class_operations import add_class
from app.operations.grade_operations import (
    add_grade,
    get_grades_by_student_and_class_id,
    update_student_grade,
)
from app.operations.user_operations import add_user
from extensions import db

STUDENT_NAME = ("Alice", "Smith")


@pytest.fixture
def setup_teacher(test_client):
    """Create a user and returns their ID."""
    teacher_id = add_user("John", "Doe", "teacher_pic_url", UserType.TEACHER, UserLevel.NA)
    return teacher_id


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
def setup_grade(test_client, setup_student, setup_class):
    """Fixture to create a grade and return its instance."""
    grade = add_grade(setup_student, setup_class, grade_value=17)
    yield grade

    db.session.delete(grade)
    db.session.commit()


def test_add_grade(test_client, setup_student, setup_class):
    """Test adding a grade for a student in a class."""
    grade_value = 85
    grade = add_grade(setup_student, setup_class, grade_value)
    assert grade is not None
    assert grade.grade == grade_value


def test_get_grades_by_student_and_class_id(test_client, setup_student, setup_class, setup_grade):
    """Test retrieving grades for a specific student in a specific class."""
    grades = get_grades_by_student_and_class_id(setup_student, setup_class)
    assert grades is not None
    assert isinstance(grades, list)
    assert len(grades) == 1
    assert grades[0].grade == setup_grade.grade


def test_update_student_grade(test_client, setup_student, setup_class):
    """Test updating the grade for a specific student in a specific class."""
    new_grade_value = 8
    success = update_student_grade(setup_class, setup_student, new_grade_value)
    assert success is True