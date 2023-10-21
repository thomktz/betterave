import pytest
from backend.app.operations import class_operations
from app.models.user import UserType, UserLevel
from backend.app.operations.user_operations import add_user

# Constants
TEACHER_NAME = ("John", "Doe")
CLASS_NAMES = ["Econometrics", "Statistics", "Microeconomics", "Machine Learning"]
ECTS_VALUES = [2, 2.5, 3, 4]
BACKGROUND_COLOR = "#FFFFFF"

@pytest.fixture
def setup_teacher(test_client):
    """Creates a teacher and returns their ID."""
    return add_user(TEACHER_NAME[0], TEACHER_NAME[1], "teacher_pic_url", UserType.TEACHER, UserLevel.NA)

@pytest.fixture
def setup_class(test_client, setup_teacher):
    """Creates a class and returns its ID."""
    class_id = 101
    return class_operations.add_class(class_id, CLASS_NAMES[0], ECTS_VALUES[0], setup_teacher, BACKGROUND_COLOR)

def test_add_and_get_class(test_client, setup_teacher):
    """Test adding and retrieving a class."""
    class_id = class_operations.add_class(101, CLASS_NAMES[1], ECTS_VALUES[1], setup_teacher, BACKGROUND_COLOR)
    retrieved_class = class_operations.get_class_by_id(class_id)
    assert retrieved_class.name == CLASS_NAMES[1]

def test_modify_class(test_client, setup_class):
    """Test modifying class information."""
    success = class_operations.modify_class(setup_class, {"name": CLASS_NAMES[2]})
    modified_class = class_operations.get_class_by_id(setup_class)
    assert success
    assert modified_class.name == CLASS_NAMES[2]

def test_remove_class(test_client, setup_class):
    """Test removing a class."""
    success = class_operations.remove_class(setup_class)
    deleted_class = class_operations.get_class_by_id(setup_class)
    assert success
    assert deleted_class is None

def test_authorize_and_deauthorize_teacher_for_class(test_client, setup_class, setup_teacher):
    """Test authorizing and deauthorizing a teacher for a class."""
    # Authorize teacher for the class
    authorize_success = class_operations.authorize_teacher_for_class(setup_teacher, setup_class)
    teachers = class_operations.get_authorized_teachers_for_class(setup_class)
    assert authorize_success
    assert len(teachers) == 1
    assert teachers[0].name == TEACHER_NAME[0]
    
    # Deauthorize teacher from the class
    deauthorize_success = class_operations.deauthorize_teacher_for_class(setup_teacher, setup_class)
    teachers_after_deauthorization = class_operations.get_authorized_teachers_for_class(setup_class)
    assert deauthorize_success
    assert len(teachers_after_deauthorization) == 0

def test_get_all_classes(test_client, setup_teacher):
    """Test retrieving all classes."""
    class_ids = [class_operations.add_class(101 + i, CLASS_NAMES[i], ECTS_VALUES[i % len(ECTS_VALUES)], setup_teacher, BACKGROUND_COLOR) for i in range(len(CLASS_NAMES))]
    classes = class_operations.get_all_classes()
    assert len(classes) == len(CLASS_NAMES)
