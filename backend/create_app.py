import os
from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, login_manager

from app.routes import bp as auth_bp
from app.routes.api_routes import *
from app.routes.auth_routes import *

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))

def create_app():
    """Function to create app instance"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or b'\x05\xe1C\x07k\x1ay<\xb6\xa4\xf8\xc6\xa8f\xb4*'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
    app.config.update(
        DEBUG=True,
        SESSION_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
    )

    CORS(app, supports_credentials=True, resources={r"/*": {
        "origins": "http://127.0.0.1:8080",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept"],
        "expose_headers": ["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"],
    }})


    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    

    return app
