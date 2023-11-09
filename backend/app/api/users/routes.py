# routes.py
from datetime import datetime
from flask_restx import Resource
from .models import user_model, user_full_model, user_classgroups_model
from .namespace import api
from app.operations.user_operations import ( 
    get_all_users,
    add_user,
    get_user_by_id,
    update_user,
    delete_user,
    authenticate_user
)
from app.operations.lesson_operations import (
    get_student_lessons,
    get_teacher_lessons,
    get_student_future_lessons,
    get_teacher_future_lessons
)
from app.api.lessons.models import lesson_model
from app.decorators import require_authentication, current_user_required

@api.route('/')
class UserList(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return get_all_users()

    @api.doc(security='apikey')
    @require_authentication('admin')
    @api.expect(user_full_model)
    def post(self):
        """Create a new user"""
        # Extract the fields from the api.payload
        data = api.payload
        user_id = add_user(**data)
        if user_id == -1:
            api.abort(400, 'Error creating user.')
        return {'message': 'User created successfully', 'user_id': user_id}, 201

@api.route('/<int:user_id>')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Fetch a user given its identifier"""
        user = get_user_by_id(user_id)
        if user is None:
            api.abort(404, 'User not found')
        return user

    @api.expect(user_full_model)
    @api.response(204, 'User updated successfully')
    @api.doc(security='apikey')
    @require_authentication("admin")
    def put(self, user_id):
        """Update a user given its identifier"""
        user = update_user(user_id, api.payload)
        if not user:
            api.abort(400, 'Error updating user.')
        return {'message': 'User updated successfully'}, 204

    @api.doc(security='apikey')
    @require_authentication("admin")
    @api.response(204, 'User deleted successfully')
    def delete(self, user_id):
        """Delete a user given its identifier"""
        success = delete_user(user_id)
        if not success:
            api.abort(400, 'Error deleting user.')
        return {'message': 'User deleted successfully'}, 204

@api.route('/<int:user_id>/classgroups')
@api.response(404, 'User not found')
@api.response(200, 'Success')
class UserClassGroupsResource(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @current_user_required
    @api.marshal_with(user_classgroups_model)
    def get(self, user_id):
        """
        Get detailed information about a user by their ID, including class associations.
        """
        user = get_user_by_id(user_id)
        if not user:
            api.abort(404, "User not found")
        user_details = {
            "id": user.user_id,
            "name": user.name,
            "surname": user.surname,
            "classgroups": [
                {
                    "class_id": class_group.class_id,
                    "class_name": class_group.class_.name,
                    "primary_class_group_id": class_group.primary_class_group_id,
                    "secondary_class_group_id": class_group.secondary_class_group_id,
                    "secondary_class_group_name": class_group.secondary_class_group.name if class_group.secondary_class_group else "",
                    "all_groups": [group.name for group in class_group.class_.groups if not group.is_main_group]
                }
                for class_group in user.class_groups
            ]
        }

        return user

@api.route('/<int:user_id>/lessons')
class UserLessons(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @current_user_required
    @api.marshal_list_with(lesson_model)
    def get(self, user_id):
        """
        Get a list of lessons for a specific student or teacher
        """
        user = get_user_by_id(user_id)

        if user.user_type.value == 'student':
            lessons = get_student_lessons(user)
        elif user.user_type.value == 'teacher':
            lessons = get_teacher_lessons(user)
        else:
            lessons = []

        return lessons

@api.route('/<int:user_id>/lessons/future')
class UserFutureLessons(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @current_user_required
    @api.marshal_list_with(lesson_model)
    def get(self, user_id):
        """
        Get a list of future lessons for a specific student or teacher
        """
        user = get_user_by_id(user_id)
        
        if user.user_type.value == 'student':
            future_lessons = get_student_future_lessons(user, datetime.now())
        elif user.user_type.value == 'teacher':
            future_lessons = get_teacher_future_lessons(user, datetime.now())
        else:
            future_lessons = []

        return future_lessons