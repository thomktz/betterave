# flake8: noqa
import pytest

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "backend"))

from main import app
from extensions import db

os.environ["API_KEY"] = "BETTERAVEAPIKEY9999" # It sets to None when it runs

@pytest.fixture(scope="function")
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    context = app.app_context()
    context.push()
    with app.test_client() as client:
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()
    context.pop()
