
from datetime import datetime
from . import bp
from flask import jsonify
from flask_login import login_required, current_user
from app.database.operations import get_lessons_by_user

@bp.route('/profile', methods=['GET'])
@login_required
def profile_route():
    return jsonify(
        email=current_user.email,
        name=current_user.name,
        status="success",
    ), 200
    
@bp.route('/lessons', methods=['GET'])
@login_required
def get_lessons_route():
    lessons = get_lessons_by_user(current_user.user_id)
    formatted_lessons = [
        {
            'id': str(lesson.lesson_id),
            'start': datetime.combine(lesson.date, lesson.start_time).isoformat(),
            'end': datetime.combine(lesson.date, lesson.end_time).isoformat(),
            'title': lesson.class_ref.name,
            "color": lesson.class_ref.backgroundColor,
        }
        for lesson in lessons
    ]
    return jsonify(formatted_lessons), 200


