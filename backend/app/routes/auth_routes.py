from . import bp
from flask import request, jsonify
from flask_login import login_user, current_user, logout_user
from app.database.operations import check_password
from app.models.student import Student

@bp.route('/login', methods=['POST'])
def login_user_route():
    if current_user.is_authenticated:
        return jsonify(message="User already logged in", status="success"), 200
    data = request.get_json()
    email = data['email']
    password = data['password']
    student = Student.query.filter_by(email=email).first()
    if student and check_password(student.hashed_password, password):
        login_user(student)
        return jsonify(message="Login successful", status="success"), 200
    else:
        return jsonify(message="Login unsuccessful. Please check email and password", status="error"), 401
    

@bp.route('/logout', methods=['POST'])
def logout_user_route():
    # Clear the Flask-Login session
    logout_user()
    # Respond to the client
    return jsonify(message="Logged out successfully", status="success"), 200