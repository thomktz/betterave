
from datetime import datetime
from . import bp
from flask import jsonify, request
from flask_login import login_required, current_user
from app.operations.class_operations import get_class_by_id
from app.operations.message_operations import get_class_messages, add_class_message
from app.operations.student_operations import get_student_lessons, get_all_students, is_student_in_class
from app.models.class_ import Class

@bp.route("/profile", methods=["GET"])
@login_required
def profile_route():
    return jsonify(
        email=current_user.email,
        name=current_user.name,
        profile_pic=current_user.profile_pic,
        status="success",
    ), 200

    
@bp.route("/lessons", methods=["GET"])
@login_required
def get_lessons_route():
    lessons = get_student_lessons(current_user.user_id)
    formatted_lessons = [
        {
            "id": lesson.lesson_id,
            "class_id": lesson.class_id,
            "start": datetime.combine(lesson.date, lesson.start_time).isoformat(),
            "end": datetime.combine(lesson.date, lesson.end_time).isoformat(),
            "title": lesson.course.name,
            "color": lesson.course.backgroundColor,
            "room": lesson.room,
            "teacher_id": lesson.teacher_id,
        }
        for lesson in lessons
    ]
    return jsonify(formatted_lessons), 200

@bp.route('/photochart', methods=['GET'])
@login_required
def all_students_route():
    students = get_all_students()
    formatted_students = [
        {
            'id' : student.user_id,
            'name': student.name,
            "surname": student.surname,
            'level' : str(student.level),
            'profile_pic': student.profile_pic
        }
        for student in students
    ]
    return jsonify(formatted_students), 200

@bp.route("/class/<int:class_id>", methods=["GET"])
@login_required
def get_class_detail(class_id):
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

@bp.route('/classes/<int:class_id>/messages', methods=['GET'])
@login_required
def get_messages(class_id):
    # Check if the user is part of the class
    if not is_student_in_class(current_user, class_id):
        return jsonify(message="Unauthorized. User not part of the class.", status="error"), 403
    
    messages = get_class_messages(class_id)
    return jsonify([msg.as_dict() for msg in messages])

@bp.route('/classes/<int:class_id>/messages', methods=['POST'])
@login_required
def post_message(class_id):
    # Check if the user is part of the class
    if not is_student_in_class(current_user, class_id):
        return jsonify(message="Unauthorized. User not part of the class.", status="error"), 403
    
    data = request.get_json()
    msg = add_class_message(data['content'], class_id, current_user.user_id)
    return jsonify(msg.as_dict()), 201

