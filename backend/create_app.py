"""App factory module."""

import os

from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from extensions import db, bcrypt, login_manager, api

from app.api import (
    auth_ns,
    users_ns,
    classes_ns,
    lessons_ns,
    class_groups_ns,
    user_class_groups_ns,
    events_ns,
)


@login_manager.user_loader
def load_user(user_id):
    """Load the user from the database."""
    from app.models.user import User

    return User.query.get(int(user_id))


def create_app():
    """Create the applicaiton instance."""
    print(f"Creating app from {os.getcwd()}", flush=True)
    print("API KEY:", os.environ.get("API_KEY"))

    # Initialize the Flask app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or b"\x05\xe1C\x07k\x1ay<\xb6\xa4\xf8\xc6\xa8f\xb4*"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////database/betterave.db"
    app.config.update(
        DEBUG=True,
        SESSION_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
    )
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:8080",
                    "http://127.0.0.1:8080",
                    "https://betterave.kientz.net",
                    "http://89.168.39.28:8080" "https://89.168.39.28:8080",
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                    "X-Requested-With",
                    "Accept",
                ],
                "expose_headers": [
                    "Access-Control-Allow-Origin",
                    "Access-Control-Allow-Credentials",
                ],
            }
        },
    )

    # Initialize the extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    api.init_app(app)

    # Initialize the Flask-RestX Api and register the namespaces
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(users_ns, path="/users")
    api.add_namespace(classes_ns, path="/classes")
    api.add_namespace(lessons_ns, path="/lessons")
    api.add_namespace(class_groups_ns, path="/class_groups")
    api.add_namespace(user_class_groups_ns, path="/user_class_groups")
    api.add_namespace(events_ns, path="/events")

    # Load/create the database
    with app.app_context():
        db.create_all()
        db.session.commit()

    # For testing purposes
    @app.route("/hello")
    def index():
        """Route for testing purposes."""
        return "Hello, World!"

    return app
