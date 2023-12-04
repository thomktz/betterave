import pytest
from backend.app.operations import user_operations
from app.operations.asso_operations import (
    subscribe_to_asso,
    unsubscribe_from_asso,
    get_all_assos,
)
from app.operations.user_operations import get_user_by_id
from app.models import UserType, UserLevel


# Constants
ASSO_NAME = "EFI"
ASSO_EMAIL = "efi@ensae.fr"
USER_NAME = ("Alice", "Smith")


# Fixtures
@pytest.fixture
def setup_user(test_client):
    """Creates a user and returns their ID."""
    student_id = user_operations.add_user(USER_NAME[0], USER_NAME[1], "student_pic_url", UserType.STUDENT, UserLevel.NA)
    return student_id


@pytest.fixture
def setup_asso(test_client):
    """Creates an Asso and returns its ID."""
    asso_id = user_operations.add_user(
        ASSO_NAME,
        "",
        "asso_pic_url",
        UserType.ASSO,
        UserLevel.NA,
        email_override=ASSO_EMAIL,
        website="https://efi.ensae.fr",
    )
    return asso_id


# Tests
def test_subscribe_to_asso(setup_user, setup_asso):
    """Subscribes a user to an asso."""
    user_id = setup_user
    asso_id = setup_asso

    assert subscribe_to_asso(user_id, asso_id) is True
    user = get_user_by_id(user_id)
    asso = get_user_by_id(asso_id)
    assert asso in user.subscriptions


def test_already_subscribed_to_asso(setup_user, setup_asso):
    """Tests subscribing a user to an asso when they're already subscribed."""
    user_id = setup_user
    asso_id = setup_asso

    # First subscription
    assert subscribe_to_asso(user_id, asso_id) is True
    # Try subscribing again
    assert subscribe_to_asso(user_id, asso_id) is True


def test_unsubscribe_from_asso(setup_user, setup_asso):
    """Tests unsubscribing a user from an asso."""
    user_id = setup_user
    asso_id = setup_asso
    # First, we need to subscribe the user
    assert subscribe_to_asso(user_id, asso_id) is True
    # Then, we'll test the unsubscription
    assert unsubscribe_from_asso(user_id, asso_id) is True
    user = get_user_by_id(user_id)
    asso = get_user_by_id(asso_id)
    assert asso not in user.subscriptions


def test_not_subscribed_unsubscribe_from_asso(setup_user, setup_asso):
    """Tests unsubscribing a user from an asso when they're not subscribed."""
    user_id = setup_user
    asso_id = setup_asso

    # Try unsubscribing without being subscribed
    assert unsubscribe_from_asso(user_id, asso_id) is True


def test_get_all_assos(setup_asso):
    """Tests retrieving all assos."""
    assos = get_all_assos()
    assert len(assos) >= 1
    for asso in assos:
        assert asso.is_asso
