"""Remove the database and create a new empty one."""

from create_app import create_app
from betterave_backend.extensions import db
import os

app = create_app()

with app.app_context():
    os.remove("/database/betterave.db")
    db.create_all()
