import functools

from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flasks.db import get_db

bp = Blueprint('student', __name__, url_prefix='/student')

def login_required(view):
    """View decorator that redirects anonymous students to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.student is None:
            return redirect(url_for('student.login'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_student():
    """If a student id is stored in the session, load the student object from
    the database into ``g.student``."""
    student_id = session.get('student_id')

    if student_id is None:
        g.student = None
    else:
        g.student = get_db().execute(
            'SELECT * FROM Student WHERE StudentId = ?', (student_id,)
        ).fetchone()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new student.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT StudentId FROM Student WHERE Username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            
            values = ()
            for key in request.form:
                if key == 'password':
                    values += (generate_password_hash(request.form[key]),)
                else:
                    values += (request.form[key],)

            db.execute(
                'INSERT INTO Student (Username, Password, Firstname, Lastname, Nickname, Birthday, Email, TelNum) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', values)
            db.commit()
        
            return redirect(url_for('student.login'))

        flash(error)

    return render_template('student/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered student by adding the student id to the session."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        student = db.execute(
            'SELECT * FROM Student WHERE Username = ?', (username,)
        ).fetchone()

        if student is None:
            error = 'Incorrect username.'
        elif not check_password_hash(student['Password'], password):
            error = 'Incorrect password.'

        if error is None:
            # store the student id in a new session and return to the index
            session.clear()
            session['student_id'] = student['StudentId']
            return redirect(url_for('hello'))

        flash(error)
    
    return render_template('student/login.html')

@bp.route('/logout')
def logout():
    """Clear the current session, including the stored student id."""
    session.clear()
    return redirect(url_for('hello'))

