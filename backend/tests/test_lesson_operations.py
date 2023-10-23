import pytest
from backend.app.operations import lesson_operations, user_operations
from app.models.user import UserType, UserLevel
from datetime import date, time

# Constants
CLASS_ID = 101
LESSON_DATE = date(2023, 10, 21)
START_TIME = time(9, 0, 0)
END_TIME = time(10, 0, 0)
STUDENT_NAME = ("Alice", "Smith")

@pytest.fixture
def setup_lesson(test_client):
    """Creates a lesson and returns its ID."""
    return lesson_operations.add_lesson(CLASS_ID, LESSON_DATE, START_TIME, END_TIME)

@pytest.fixture
def setup_student_instance(test_client):
    """Creates a student and returns their instance."""
    student_id = user_operations.add_user(STUDENT_NAME[0], STUDENT_NAME[1], "student_pic_url", UserType.STUDENT, UserLevel.NA)
    return user_operations.get_user_by_id(student_id)

def test_add_and_get_lesson(test_client):
    """Test adding and retrieving a lesson."""
    lesson_id = lesson_operations.add_lesson(CLASS_ID, LESSON_DATE, START_TIME, END_TIME)
    retrieved_lesson = lesson_operations.get_lesson_by_id(lesson_id)
    assert retrieved_lesson.date == LESSON_DATE

def test_modify_lesson(test_client, setup_lesson):
    """Test modifying lesson information."""
    success = lesson_operations.modify_lesson(setup_lesson, {"date": LESSON_DATE})
    modified_lesson = lesson_operations.get_lesson_by_id(setup_lesson)
    assert success
    assert modified_lesson.date == LESSON_DATE

def test_remove_lesson(test_client, setup_lesson):
    """Test removing a lesson."""
    success = lesson_operations.remove_lesson(setup_lesson)
    deleted_lesson = lesson_operations.get_lesson_by_id(setup_lesson)
    assert success
    assert deleted_lesson is None

def test_assign_students_to_lesson(test_client, setup_lesson, setup_student_instance):
    """Test assigning students to a lesson."""
    students = [setup_student_instance]
    success = lesson_operations.assign_students_to_lesson(setup_lesson, students)
    assert success

def test_add_student_to_lesson(test_client, setup_lesson, setup_student_instance):
    """Test adding a single student to a lesson."""
    success = lesson_operations.add_student_to_lesson(setup_lesson, setup_student_instance)
    assert success

def test_get_all_lessons(test_client, setup_lesson):
    """Test retrieving all lessons."""
    lessons = lesson_operations.get_all_lessons()
    assert len(lessons) > 0

def test_get_lessons_by_class_id(test_client, setup_lesson):
    """Test getting lessons by class ID."""
    lessons = lesson_operations.get_lessons_by_class_id(CLASS_ID)
    assert len(lessons) > 0

def test_get_lessons_by_student_id(test_client, setup_lesson, setup_student_instance):
    """Test getting lessons by student ID."""
    student_id = setup_student_instance.user_id
    lesson_operations.add_student_to_lesson(setup_lesson, setup_student_instance)
    lessons = lesson_operations.get_lessons_by_student_id(student_id)
    assert len(lessons) > 0
