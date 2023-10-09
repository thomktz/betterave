from flask import Blueprint, request, jsonify, make_response
from flask_login import login_user, login_required, current_user, logout_user
from app.database.operations import check_password
from app.models.student import Student

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
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

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    # You can send back user-related data here, e.g., name, email, etc.
    return jsonify(
        email=current_user.email,
        name=current_user.name,
        status="success"
    ), 200

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(message="Logged out successfully", status="success"), 200
