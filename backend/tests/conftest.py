# flake8: noqa
import pytest

import sys
import os

sys.path.append(os.getcwd())

from main import app
from extensions import db


@pytest.fixture(scope="function")
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    context = app.app_context()
    context.push()
    with app.test_client() as client:
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()
    context.pop()
