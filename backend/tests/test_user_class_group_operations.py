# type: ignore
import pytest
from app.models import UserType, UserLevel
from app.operations.user_class_group_operations import (
    add_user_class_group,
    delete_user_class_group,
    get_user_class_group_by_id,
)
from app.operations.class_group_operations import add_class_group, delete_class_group
from app.operations.user_operations import add_user, delete_user, get_user_by_id
from app.operations.class_operations import add_class

# Constants for the test
PRIMARY_GROUP_NAME = "Test Primary Group"
SECONDARY_GROUP_NAME = "Test Secondary Group"
CLASS_ID = 0
CLASS_NAME = "Test Class"
LEVEL = "1A"
USER_ID = 0
ECTS_CREDITS = 3
NAME = "John"
SURNAME = "Doe"
USER_TYPE = UserType.STUDENT
USER_LEVEL = UserLevel._1A


@pytest.fixture
def setup_teacher(test_client):
    """Create a user and returns their ID."""
    teacher_id = add_user("John", "Doe", "teacher_pic_url", UserType.TEACHER, UserLevel.NA)
    return teacher_id


@pytest.fixture
def setup_class(test_client, setup_teacher):
    """Create a class and returns its ID."""
    class_id = add_class(
        class_id=CLASS_ID,
        name=CLASS_NAME,
        ects_credits=ECTS_CREDITS,
        default_teacher_id=setup_teacher,
        level=LEVEL,
        background_color="#123456",
    )
    yield class_id


@pytest.fixture
def setup_primary_class_group(test_client, setup_class):
    """Create a primary group for the class."""
    primary_class_group_id = add_class_group(name=PRIMARY_GROUP_NAME, class_id=setup_class, is_main_group=True)
    yield primary_class_group_id
    delete_class_group(primary_class_group_id)


@pytest.fixture
def setup_secondary_class_group(test_client, setup_class):
    """Create a secondary group for the class."""
    secondary_class_group_id = add_class_group(name=SECONDARY_GROUP_NAME, class_id=setup_class, is_main_group=False)
    yield secondary_class_group_id
    delete_class_group(secondary_class_group_id)


@pytest.fixture
def setup_user(test_client):
    """Create a user and returns their ID."""
    user_id = add_user(
        name=NAME,
        surname=SURNAME,
        profile_pic="",
        user_type=USER_TYPE,
        level=USER_LEVEL,
    )
    yield user_id
    delete_user(user_id)


@pytest.fixture
def setup_user_class_group(test_client, setup_user, setup_primary_class_group, setup_secondary_class_group):
    """Create a UserClassGroup and returns its ID."""
    user_class_group_id = add_user_class_group(
        user_id=setup_user,
        class_id=CLASS_ID,
        primary_class_group_id=setup_primary_class_group,
        secondary_class_group_id=setup_secondary_class_group,
    )
    yield user_class_group_id
    delete_user_class_group(user_class_group_id)


def test_add_user_class_group(setup_user, setup_primary_class_group):
    """Test adding a new UserClassGroup with only a primary group."""
    user_class_group_id = add_user_class_group(
        user_id=setup_user,
        class_id=CLASS_ID,
        primary_class_group_id=setup_primary_class_group,
    )
    assert user_class_group_id != -1


def test_delete_user_class_group(setup_user_class_group):
    """Test deleting a UserClassGroup."""
    assert delete_user_class_group(setup_user_class_group) is True
    user_class_group = get_user_class_group_by_id(setup_user_class_group)
    assert user_class_group is None


def test_user_with_no_class_groups(setup_user):
    """Test retrieving a user with no class groups."""
    user = get_user_by_id(setup_user)
    assert user is not None
    class_groups = user.class_groups.all()  # Execute the query to get the list
    assert len(class_groups) == 0


def test_user_with_only_primary_class_group(setup_user, setup_primary_class_group):
    """Test retrieving a user with only a primary class group."""
    add_user_class_group(
        user_id=setup_user,
        class_id=CLASS_ID,
        primary_class_group_id=setup_primary_class_group,
    )
    user = get_user_by_id(setup_user)
    assert user is not None
    class_groups = user.class_groups.all()  # Execute the query to get the list
    assert len(class_groups) == 1
    assert class_groups[0].primary_class_group_id == setup_primary_class_group
    assert class_groups[0].secondary_class_group is None


def test_user_with_primary_and_secondary_class_groups(setup_user_class_group):
    """Test retrieving a user with both primary and secondary class groups."""
    user_class_group = get_user_class_group_by_id(setup_user_class_group)
    assert user_class_group is not None
    assert user_class_group.primary_class_group_id is not None
    assert user_class_group.secondary_class_group_id is not None
