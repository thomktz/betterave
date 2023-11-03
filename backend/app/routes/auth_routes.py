from . import bp
from flask import request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app.operations.user_operations import check_password, get_user_by_email


@bp.route("/login", methods=["POST"])
def login_user_route():
    if current_user.is_authenticated:
        return jsonify(message="User already logged in", status="success"), 200
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = get_user_by_email(email)

    if user and check_password(user.hashed_password, password):
        login_user(user)        
        return jsonify(message=user.user_type.value.capitalize() + " login successful", status="success"), 200
        
    else:
        return jsonify(message="Login unsuccessful. Please check email and password", status="error"), 401
    

@bp.route("/logout", methods=["POST"])
def logout_user_route():
    # Clear the Flask-Login session
    logout_user()
    # Respond to the client
    return jsonify(message="Logged out successfully", status="success"), 200

@bp.route("/check-auth", methods=["GET"])
def check_authentication():
    if current_user.is_authenticated:
        # Return the user's role along with the authentication status
        return jsonify({"status": "authenticated", "role": current_user.user_type.value}), 200
    else:
        # Return a non-authenticated status for unauthenticated users
        return jsonify({"status": "unauthenticated", "role": None}), 401  # 401 Unauthorized