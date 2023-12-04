import pytest
from app.operations import class_operations
from app.models import UserType, UserLevel
from app.operations.user_operations import add_user

# Constants
CLASS_NAME = "Data Science"
ECTS_CREDITS = 5
LEVEL = "1A"
BACKGROUND_COLOR = "#123456"


@pytest.fixture
def setup_teacher(test_client):
    """Create a user and returns their ID."""
    student_id = add_user("John", "Doe", "teacher_pic_url", UserType.TEACHER, UserLevel.NA)
    return student_id


@pytest.fixture
def setup_class(test_client, setup_teacher):
    """Fixture to create a class and return its instance."""
    class_id = class_operations.add_class(
        class_id=0,
        name=CLASS_NAME,
        ects_credits=ECTS_CREDITS,
        default_teacher_id=setup_teacher,
        level=LEVEL,
        background_color=BACKGROUND_COLOR,
    )
    return class_operations.get_class_by_id(class_id)


def test_add_class(setup_teacher):
    """Test adding a class."""
    class_id = class_operations.add_class(
        class_id=1,
        name=CLASS_NAME,
        ects_credits=ECTS_CREDITS,
        default_teacher_id=setup_teacher,
        level=LEVEL,
        background_color=BACKGROUND_COLOR,
    )
    assert class_id != -1
    new_class = class_operations.get_class_by_id(class_id)
    assert new_class is not None
    assert new_class.name == CLASS_NAME


def test_update_class(setup_class):
    """Test modifying class information."""
    new_name = "Advanced Data Science"
    success = class_operations.update_class(setup_class.class_id, {"name": new_name})
    assert success is True
    modified_class = class_operations.get_class_by_id(setup_class.class_id)
    assert modified_class.name == new_name


def test_delete_class(setup_class):
    """Test removing a class."""
    success = class_operations.delete_class(setup_class.class_id)
    assert success is True
    deleted_class = class_operations.get_class_by_id(setup_class.class_id)
    assert deleted_class is None


def test_get_class_by_id(setup_class):
    """Test retrieving a class by its ID."""
    result_class = class_operations.get_class_by_id(setup_class.class_id)
    assert result_class is not None
    assert result_class.class_id == setup_class.class_id
    assert result_class.name == setup_class.name


def test_get_all_classes(setup_class):
    """Test retrieving all classes."""
    all_classes = class_operations.get_all_classes()
    assert len(all_classes) > 0
    assert setup_class in all_classes
