
from datetime import datetime
from . import bp
from flask import jsonify
from flask_login import login_required, current_user
from app.database.operations import get_lessons_by_student, get_all_students
from app.models.class_ import Class

@bp.route("/profile", methods=["GET"])
@login_required
def profile_route():
    return jsonify(
        email=current_user.email,
        name=current_user.name,
        profil_pic=current_user.profile_pic,
        status="success",
    ), 200

    
@bp.route("/lessons", methods=["GET"])
@login_required
def get_lessons_route():
    lessons = get_lessons_by_student(current_user.student_id)
    formatted_lessons = [
        {
            "id": str(lesson.lesson_id),
            "class_id": str(lesson.class_id),
            "start": datetime.combine(lesson.date, lesson.start_time).isoformat(),
            "end": datetime.combine(lesson.date, lesson.end_time).isoformat(),
            "title": lesson.class_ref.name,
            "color": lesson.class_ref.backgroundColor,
            "room": lesson.room,
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
            'id' : student.student_id,
            'name': student.name,
            "surname": student.surname,
            'level' : student.level,
            'profile_pic': student.profile_pic
        }
        for student in students
    ]
    return jsonify(formatted_students), 200

@bp.route("/class/<int:class_id>", methods=["GET"])
def get_class_detail(class_id):
    class_instance = Class.query.get(class_id)
    if class_instance:
        # serialize and send data
        return jsonify({
            "name": class_instance.name,
            "ects_credits": class_instance.ects_credits,
            "ensae_link": class_instance.ensae_link,
            "tutor": class_instance.tutor,
            "backgroundColor": class_instance.backgroundColor
        }), 200
    else:
        return jsonify(message="Class not found", status="error"), 404
