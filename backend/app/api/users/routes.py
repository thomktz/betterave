# routes.py
from datetime import datetime
from flask_restx import Resource
from .models import (
    user_model, 
    user_full_model, 
    user_classgroups_model, 
    asso_model,
)
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
    get_all_lessons,
    get_student_future_lessons,
    get_teacher_future_lessons,
    get_all_future_lessons,
)
from app.operations.asso_operations import (
    get_all_assos,
    unsubscribe_from_asso,
    subscribe_to_asso,
)
from app.operations.event_operations import (
    get_association_events,
    get_all_events,
    get_user_events,
    get_association_future_events,
    get_all_future_events,
    get_user_future_events,
)
from app.api.lessons.models import fullcalendar_lesson_model
from app.api.events.models import fullcalendar_event_model
from app.decorators import require_authentication, current_user_required, resolve_user

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

@api.route('/<string:user_id_or_me>')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @resolve_user
    @api.marshal_with(user_model)
    def get(self, user):
        """Fetch a user given its identifier"""
        return user

    @api.expect(user_full_model)
    @api.response(204, 'User updated successfully')
    @api.doc(security='apikey')
    @require_authentication()
    @resolve_user
    @current_user_required
    def put(self, user):
        """Update a user given its identifier"""
        if not update_user(user, api.payload):
            api.abort(400, 'Error updating user.')
        return {'message': 'User updated successfully'}, 204

    @api.doc(security='apikey')
    @api.response(204, 'User deleted successfully')
    @require_authentication("admin")
    def delete(self, user_id_or_me):
        """Delete a user given its identifier"""
        print("Deleting user", user_id_or_me, flush=True)
        if not delete_user(int(user_id_or_me)):
            api.abort(400, 'Error deleting user.')
        return {'message': 'User deleted successfully'}, 204

@api.route('/<string:user_id_or_me>/classgroups')
@api.response(404, 'User not found')
@api.response(200, 'Success')
class UserClassGroupsResource(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @resolve_user
    @current_user_required
    @api.marshal_with(user_classgroups_model)
    def get(self, user):
        """
        Get detailed information about a user by their ID, including class associations.
        """
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

        return user_details

@api.route('/<string:user_id_or_me>/lessons')
class UserLessons(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @resolve_user
    @current_user_required
    @api.marshal_list_with(fullcalendar_lesson_model)
    def get(self, user):
        """
        Get a list of lessons for a specific student or teacher
        """
        if user.is_student:
            lessons = get_student_lessons(user)
        elif user.is_teacher:
            lessons = get_teacher_lessons(user)
        elif user.is_admin:
            lessons = get_all_lessons()
        else:
            lessons = []

        return lessons

@api.route('/<string:user_id_or_me>/lessons/future')
class UserFutureLessons(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @resolve_user
    @current_user_required
    @api.marshal_list_with(fullcalendar_lesson_model)
    def get(self, user):
        """
        Get a list of future lessons for a specific student or teacher
        """
        if user.is_student:
            future_lessons = get_student_future_lessons(user)
        elif user.is_teacher:
            future_lessons = get_teacher_future_lessons(user)
        elif user.is_admin:
            future_lessons = get_all_future_lessons()
        else:
            future_lessons = []

        return future_lessons
    
@api.route('/associations')
class AssociationList(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @api.marshal_list_with(asso_model)
    def get(self):
        """Get a list of all associations"""
        associations = get_all_assos()
        return associations
    
@api.route('/associations/<string:user_id_or_me>')
class UserAssociationList(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @resolve_user
    @current_user_required
    def get(self, user):
        """Get a list of all associations with subscription status for a specific user"""
        associations = get_all_assos()

        marshalled = api.marshal(associations, asso_model)
        for marshalled_asso, asso in zip(marshalled, associations):
            marshalled_asso['subscribed'] = (user in asso.subscribers)
        return marshalled
    
@api.route('/<string:user_id_or_me>/subscribe/<int:asso_id>')
class SubscribeAssociation(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @resolve_user
    def post(self, user, asso_id):
        """Subscribe a user to an association"""
        asso = get_user_by_id(asso_id)
        if not asso:
            api.abort(404, "Association not found")
        if not asso.is_asso:
            api.abort(400, f"User asso_id={asso_id} is not an association")
        if subscribe_to_asso(user, asso):
            return {"message": "User subscribed successfully to the association"}, 200
        else:
            api.abort(400, "Could not subscribe user to the association")

@api.route('/<string:user_id_or_me>/unsubscribe/<int:asso_id>')
class UnsubscribeAssociation(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @resolve_user
    def post(self, user, asso_id):
        """Unsubscribe a user from an association"""
        asso = get_user_by_id(asso_id)
        if not asso:
            api.abort(404, "Association not found")
        if not asso.is_asso:
            api.abort(400, f"User asso_id={asso_id} is not an association")
        if unsubscribe_from_asso(user, asso):
            return {"message": "User unsubscribed successfully from the association"}, 200
        else:
            api.abort(400, "Could not unsubscribe user from the association")
            
@api.route('/<string:user_id_or_me>/events')
class UserEvents(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @resolve_user
    @current_user_required
    @api.marshal_list_with(fullcalendar_event_model)
    def get(self, user):
        """
        Get a list of events for a specific user
        """
        if user.is_asso:
            events = get_association_events(user)
        elif user.is_admin:
            events = get_all_events()
        else:
            events = get_user_events(user)

        return events

@api.route('/<string:user_id_or_me>/events/future')
class UserFutureEvents(Resource):
    @api.doc(security='apikey')
    @require_authentication()
    @resolve_user
    @current_user_required
    @api.marshal_list_with(fullcalendar_event_model)
    def get(self, user_id):
        """
        Get a list of future events for a specific user
        """        
        if user.is_asso:
            future_events = get_association_future_events(user)
        elif user.is_admin:
            future_events = get_all_future_events()
        else:
            future_events = get_user_future_events(user)

        return future_events