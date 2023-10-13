from . import bp
from flask import request, jsonify
from flask_login import login_user, current_user, logout_user
from app.database.operations import check_password
from app.models.user import User


@bp.route('/login', methods=['POST'])

def login_user_route():
    if current_user.is_authenticated:
        return jsonify(message="User already logged in", status="success"), 200
    data = request.get_json()
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
        
    else:
        return jsonify(message="Login unsuccessful. Please check email and password", status="error"), 401
    

@bp.route('/logout', methods=['POST'])
def logout_user_route():
    # Clear the Flask-Login session
    logout_user()
    # Respond to the client
    return jsonify(message="Logged out successfully", status="success"), 200