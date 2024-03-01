# type: ignore
from backend.app.models import UserLevel, UserType
from backend.app.operations import user_operations

PIC_URL = "pic_url"


def test_add_and_get_user_by_id(test_client):
    """Test adding a user and retrieving them by ID."""
    user_id = user_operations.add_user("Alice", "Bob", PIC_URL, UserType.STUDENT, UserLevel._1A)
    user = user_operations.get_user_by_id(user_id)
    assert user.name == "Alice"


def test_update_user(test_client):
    """Test modifying user details."""
    user_id = user_operations.add_user("Alice", "Bob", PIC_URL, UserType.STUDENT, UserLevel._1A)
    modification_success = user_operations.update_user(user_id, {"name": "Alicia"})
    user = user_operations.get_user_by_id(user_id)
    assert modification_success
    assert user.name == "Alicia"


def test_delete_user(test_client):
    """Test deleting a user by ID."""
    user_id = user_operations.add_user("Charlie", "Doe", PIC_URL, UserType.TEACHER, UserLevel.NA)
    delete_success = user_operations.delete_user(user_id)
    user = user_operations.get_user_by_id(user_id)
    assert delete_success
    assert user is None


def test_get_user_by_email(test_client):
    """Test retrieving a user by their email."""
    user_operations.add_user(
        "David",
        "Eliot",
        PIC_URL,
        UserType.STUDENT,
        UserLevel._3A,
        email_override="david.eliot@example.com",
    )
    user = user_operations.get_user_by_email("david.eliot@example.com")
    assert user.name == "David"


def test_get_all_users(test_client):
    """Test retrieving all users."""
    user_operations.add_user("Eva", "Finn", PIC_URL, UserType.ADMIN, UserLevel.NA)
    user_operations.add_user("Gary", "Holt", PIC_URL, UserType.ASSO, UserLevel.NA)
    users = user_operations.get_all_users()
    assert len(users) == 2


def test_get_user_profile_pic(test_client):
    """Test retrieving a user's profile picture."""
    user_id = user_operations.add_user("Ian", "Jolt", "special_pic", UserType.TEACHER, UserLevel.NA)
    profile_pic = user_operations.get_user_profile_pic(user_id)
    assert profile_pic == "special_pic"


def test_get_user_by_name(test_client):
    """Test retrieving a user by their full name."""
    user_operations.add_user("Katy", "Levi", PIC_URL, UserType.STUDENT, UserLevel._3A)
    user = user_operations.get_user_by_name("Katy", "Levi")
    assert user.name == "Katy"
