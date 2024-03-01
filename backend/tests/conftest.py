# type: ignore
# flake8: noqa
import pytest
import sys
import os

sys.path.append(os.path.join(os.getcwd(), "backend"))

from backend.create_app import create_app
from backend.extensions import db


@pytest.fixture(scope="function")
def test_client():
    app = create_app(db_test_path="sqlite:///:memory:")

    context = app.app_context()
    context.push()
    with app.test_client() as client:
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()
    context.pop()
