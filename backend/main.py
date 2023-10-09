from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from app.models.student import Student
    return Student.query.get(int(user_id))

from app.routes.auth_routes import bp as auth_bp
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
