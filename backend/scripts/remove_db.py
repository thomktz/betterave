# reset_db.py
from create_app import create_app
from extensions import db
import os

app = create_app()

with app.app_context():
    os.remove('/database/betterave.db')
    db.create_all()