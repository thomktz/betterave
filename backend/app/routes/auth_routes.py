from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, current_user
from app.database.operations import check_password
from app.models.student import Student
from main import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        student = Student.query.filter_by(email=email).first()
        if student and check_password(student.hashed_password, password):
            login_user(student)
            return redirect(url_for('auth.profile'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
