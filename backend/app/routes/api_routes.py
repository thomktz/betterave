
from datetime import datetime
from functools import wraps
from . import bp
from flask import jsonify, request
from flask_login import login_required, current_user
from app.models import ClassGroup
from app.decorators import type_required
from app.operations.class_operations import get_class_by_id
from app.operations.message_operations import get_class_messages, add_class_message
from app.operations.student_operations import get_student_lessons, get_all_students, is_student_in_class
from app.operations.asso_operations import subscribe_to_asso, unsubscribe_from_asso, get_all_assos
from app.operations.event_operations import add_event
from app.operations.user_operations import get_all_users, delete_user, add_user, get_user_by_id, modify_user
from app.operations.user_class_group_operations import get_ucg_by_user_and_class, modify_user_class_group

@bp.route("/profile", methods=["GET"])
@login_required
def profile_route():
    print("Getting profile for user", current_user.name, current_user.surname)
    return jsonify(
        email=current_user.email,
        name=current_user.name,
        profile_pic=current_user.profile_pic,
        user_type=current_user.user_type.value,
        status="success",
    ), 200

@bp.route("/lessons", methods=["GET"])
@login_required
def get_lessons_route():
    print("Getting lessons for user", current_user.name, current_user.surname)
    lessons = get_student_lessons(current_user)
    formatted_lessons = [
        {
            "id": lesson.lesson_id,
            "group_id": lesson.group_id,
            "class_id": lesson.class_group.class_id,
            "start": datetime.combine(lesson.date, lesson.start_time).isoformat(),
            "end": datetime.combine(lesson.date, lesson.end_time).isoformat(),
            "title": lesson.class_group.class_ref.name,
            "type": lesson.class_group.name,
            "color": lesson.class_group.class_ref.backgroundColor,
            "room": lesson.room,
            "teacher_id": lesson.teacher_id,
        }
        for lesson in lessons
    ]
    return jsonify(formatted_lessons), 200

@bp.route("/photochart", methods=["GET"])
@login_required
def all_students_route():
    print("Getting all students")
    students = get_all_students()
    formatted_students = [
        {
            "id" : student.user_id,
            "name": student.name,
            "surname": student.surname,
            "level" : student.level.value,
            "profile_pic": student.profile_pic
        }
        for student in students
    ]
    return jsonify(formatted_students), 200

@bp.route("/class/<int:class_id>", methods=["GET"])
@login_required
def get_class_detail(class_id):
    print("Getting class detail for class", class_id)
    class_instance = get_class_by_id(class_id)
    if class_instance:
        return jsonify({
            "name": class_instance.name,
            "ects_credits": class_instance.ects_credits,
            "ensae_link": class_instance.ensae_link,
            "teacher": class_instance.default_teacher.name + " " + class_instance.default_teacher.surname,
            "backgroundColor": class_instance.backgroundColor,
            "user_id": current_user.user_id,
            "user_authorised": is_student_in_class(current_user, class_id)
            # TODO: Also check if user is a teacher and is authorized too
            # -> is_student_in_class(...) or is_teacher_in_class(...)
        }), 200
    else:
        return jsonify(message="Class not found", status="error"), 404

@bp.route("/classes/<int:class_id>/messages", methods=["GET"])
@login_required
def get_messages(class_id):
    # Check if the user is part of the class
    if not is_student_in_class(current_user, class_id):
        return jsonify(message="Unauthorized. User not part of the class.", status="error"), 403
    
    messages = get_class_messages(class_id)
    return jsonify([msg.as_dict() for msg in messages])

@bp.route("/classes/<int:class_id>/messages", methods=["POST"])
@login_required
def post_message(class_id):
    # Check if the user is part of the class
    if not is_student_in_class(current_user, class_id):
        return jsonify(message="Unauthorized. User not part of the class.", status="error"), 403
    
    data = request.get_json()
    msg = add_class_message(data["content"], class_id, current_user.user_id)
    return jsonify(msg.as_dict()), 201

@bp.route("/events", methods=["POST"])
@login_required
@type_required("asso", "teacher", "admin")
def add_event_route():
    data = request.get_json()
    # TODO: Check required fields in data
    event_id = add_event(
        name=data.get("name"),
        date=data.get("date"),
        start_time=data.get("start_time"),
        end_time=data.get("end_time"),
        location=data.get("location"),
        description=data.get("description")
    )
    
    if event_id > 0:
        return jsonify(message="Event added successfully", event_id=event_id, status="success"), 201
    else:
        return jsonify(message="Error adding event", status="error"), 500

@bp.route("/assos/<int:asso_id>/subscribe", methods=["POST"])
@login_required
def subscribe_to_asso_route(asso_id):
    success = subscribe_to_asso(current_user.user_id, asso_id)
    
    if success:
        return jsonify(message="Subscribed successfully", status="success"), 200
    else:
        return jsonify(message="Error subscribing to association", status="error"), 500

@bp.route("/assos/<int:asso_id>/unsubscribe", methods=["DELETE"])
@login_required
def unsubscribe_from_asso_route(asso_id):
    success = unsubscribe_from_asso(current_user.user_id, asso_id)
    
    if success:
        return jsonify(message="Unsubscribed successfully", status="success"), 200
    else:
        return jsonify(message="Error unsubscribing from association", status="error"), 500
    
@bp.route("/assos", methods=["GET"])
@login_required
def get_all_assos_route():
    assos = get_all_assos()
    formatted_assos = [
        {
            "id": asso.user_id,
            "name": asso.name,
            "logo": asso.profile_pic,
            "linkedin": asso.linkedin,
            "subscribed": current_user in asso.subscribers  # Check if the user is a subscriber
        }
        for asso in assos
    ]
    return jsonify(formatted_assos), 200

@bp.route("/users", methods=["GET"])
@type_required("admin")
def get_users_route():
    print("Getting all users, from user", current_user.name, current_user.surname)
    users = get_all_users()
    formatted_users = [
        {
            "id": user.user_id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "level": user.level.value,
            "user_type": user.user_type.value,
            "profile_pic": user.profile_pic,
        }
        for user in users
    ]
    return jsonify(formatted_users), 200

@bp.route("/users/<int:user_id>", methods=["DELETE"])
@type_required("admin")
def delete_user_route(user_id):
    success = delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found or error deleting the user"}), 404
    
@bp.route("/users", methods=["POST"])
@type_required("admin")
def create_user_route():
    user_data = request.get_json()
    user_id = add_user(
        name=user_data["name"],
        surname=user_data["surname"],
        profile_pic=user_data.get("profile_pic", ""),
        user_type=user_data["user_type"],
        level=user_data.get("level", "N/A"),
        email_override=user_data.get("email"),
        password_override=user_data.get("password"),
        linkedin=user_data.get("linkedin"),
        website=user_data.get("website")
    )
    
    if user_id == -1:
        return jsonify({"message": "Error creating user"}), 400
    
    user = get_user_by_id(user_id)
    return jsonify({
        "id": user.user_id,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "level": user.level.value,
        "user_type": user.user_type.value,
        "profile_pic": user.profile_pic,
    }), 201

@bp.route("/users/<int:user_id>", methods=["PUT"])
@type_required("admin")
def update_user_route(user_id):
    user_data = request.get_json()
    success = modify_user(user_id, user_data)
    
    if not success:
        return jsonify({"message": "User not found or error updating the user"}), 404

    user = get_user_by_id(user_id)
    return jsonify({
        "id": user.user_id,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "level": user.level.value,
        "user_type": user.user_type.value,
        "profile_pic": user.profile_pic,
    }), 200
    
@bp.route("/users/<int:user_id>", methods=["GET"])
@type_required("admin")
def get_user_route(user_id):
    user = get_user_by_id(user_id)
    print("Getting info on user", user.name, user.surname, "from user", current_user.name, current_user.surname)
    if not user:
        return jsonify({"message": "User not found"}), 404    
    
    return jsonify({
        "id": user.user_id,
        "name": user.name,
        "surname": user.surname,
        "classes": [
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
    }), 200
    
@bp.route("/user_class_groups/<int:user_id>/<int:class_id>", methods=["PUT"])
@type_required("admin")
def update_user_class_group_by_name(user_id, class_id):
    data = request.json
    secondary_class_group_name = data.get('secondary_class_group_name')
    
    secondary_class_group = ClassGroup.query.filter_by(class_id=class_id, name=secondary_class_group_name).first()
    if not secondary_class_group:
        return jsonify({'message': 'Group not found'}), 404
    secondary_class_group_id = secondary_class_group.group_id

    user_class_group = get_ucg_by_user_and_class(user_id=user_id, class_id=class_id)
    if not user_class_group:
        return jsonify({'message': 'UserClassGroup not found'}), 404
    
    if modify_user_class_group(user_class_group, {"secondary_class_group_id": secondary_class_group_id}):
        return jsonify({"message": "UserClassGroup updated successfully"}), 200

    return jsonify({'message': 'UserClassGroup updated successfully'}), 200