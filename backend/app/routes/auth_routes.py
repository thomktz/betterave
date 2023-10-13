from . import bp
from flask import request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app.database.operations import check_password
from app.models.user import User


<<<<<<< HEAD
@bp.route('/login', methods=['POST'])

=======
@bp.route("/login", methods=["POST"])
>>>>>>> origin/main
def login_user_route():
    if current_user.is_authenticated:
        return jsonify(message="User already logged in", status="success"), 200
    data = request.get_json()
<<<<<<< HEAD
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()

    if user and check_password(user.hashed_password, password):
        print("Authentified")
        login_user(user)

        dict_user_types = {
            "student": "Student",
            "student_asso": "Student Asso",
            "teacher": "Teacher",
            "admin": "Admin"
        }

        user_type = user.user_type
        print(user_type)
        
        if user_type in dict_user_types:
            return jsonify(message=f"{dict_user_types[user_type]} login successful", status="success",userType=user_type), 200
        
=======
    email = data["email"]
    password = data["password"]
    student = Student.query.filter_by(email=email).first()
    if student and check_password(student.hashed_password, password):
        login_user(student)
        return jsonify(message="Login successful", status="success"), 200
>>>>>>> origin/main
    else:
        return jsonify(message="Login unsuccessful. Please check email and password", status="error"), 401
    

@bp.route("/logout", methods=["POST"])
def logout_user_route():
    # Clear the Flask-Login session
    logout_user()
    # Respond to the client
    return jsonify(message="Logged out successfully", status="success"), 200

@bp.route("/check-auth", methods=["GET"])
@login_required
def check_authentication():
    return jsonify(message="User is authenticated", status="authenticated"), 200