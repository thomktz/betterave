"""Flask extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_restx import Api

authorizations = {"apikey": {"type": "apiKey", "in": "header", "name": "X-API-KEY"}}

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
api = Api(
    version="3.2",
    title="Betterave API",
    description="Flask-RestX API for the Betterave app.",
    authorizations=authorizations,
    security="apikey",
)
