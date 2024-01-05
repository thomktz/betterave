# type: ignore
from flask_restx import Resource
from flask_login import login_user, current_user, logout_user
from .namespace import api
from .models import login_model, login_status_model
from app.operations.user_operations import check_password, get_user_by_email


@api.route("/login")
class LoginUser(Resource):
    @api.expect(login_model)
    def post(self):
        """Try to login user."""
        if current_user.is_authenticated:
            return {"message": "User already logged in"}, 200
        data = api.payload
        email = data["email"]
        password = data["password"]
        user = get_user_by_email(email)

        if user and check_password(user.hashed_password, password):
            login_user(user)
            return {"message": user.user_type.value.capitalize() + " login successful"}, 200
        api.abort(401, "Invalid email or password")


@api.route("/logout")
class LogoutUser(Resource):
    def post(self):
        """Logout user."""
        logout_user()
        return {"message": "Logged out successfully", "status": "success"}, 200


@api.route("/check-auth")
class CheckAuthentication(Resource):
    @api.marshal_with(login_status_model)
    def get(self):
        """Check if user is authenticated."""
        if current_user.is_authenticated:
            return {
                "status": "authenticated",
                "role": current_user.user_type.value,
            }, 200
        api.abort(401, "User not authenticated")
