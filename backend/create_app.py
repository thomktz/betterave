import os
from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, login_manager

@login_manager.user_loader
def load_user(user_id):
    from app.models.student import Student
    return Student.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or b'\x05\xe1C\x07k\x1ay<\xb6\xa4\xf8\xc6\xa8f\xb4*'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_NAME'] = 'session'
    app.config['SESSION_COOKIE_DOMAIN'] = None  # Default is None
    app.config['SESSION_COOKIE_PATH'] = '/'
    app.config['SESSION_COOKIE_HTTPONLY'] = True


    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth_routes import bp as auth_bp
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    CORS(app, supports_credentials=True, resources={r"/*": {
        "origins": "http://127.0.0.1:8080",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": "*"
    }})

    return app
