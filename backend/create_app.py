from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, login_manager

@login_manager.user_loader
def load_user(user_id):
    from app.models.student import Student
    return Student.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth_routes import bp as auth_bp
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    CORS(app, resources={r"/*": {
        "origins": "http://localhost:8080",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": "*"
    }})

    return app
