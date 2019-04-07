import functools

from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flasks.db import get_db

bp = Blueprint('teacher', __name__, url_prefix='/teacher')

def login_required(view):
    """View decorator that redirects anonymous teachers to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.teacher is None:
            return redirect(url_for('teacher.login'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_teacher():
    """If a teacher id is stored in the session, load the teacher object from
    the database into ``g.teacher``."""
    teacher_id = session.get('teacher_id')

    if teacher_id is None:
        g.teacher = None
    else:
        g.teacher = get_db().execute(
            'SELECT * FROM teacher WHERE TeacherId = ?', (teacher_id,)
        ).fetchone()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new teacher.
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
            'SELECT teacherId FROM teacher WHERE Username = ?', (username,)
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
                'INSERT INTO Teacher (Username, Password, Firstname, Lastname, Nickname, Birthday, Email, TelNum) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', values)
            db.commit()
        
            return redirect(url_for('teacher.login'))

        flash(error)

    return render_template('teacher/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered teacher by adding the teacher id to the session."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        teacher = db.execute(
            'SELECT * FROM teacher WHERE Username = ?', (username,)
        ).fetchone()

        if teacher is None:
            error = 'Incorrect username.'
        elif not check_password_hash(teacher['Password'], password):
            error = 'Incorrect password.'

        if error is None:
            # store the teacher id in a new session and return to the index
            session.clear()
            session['teacher_id'] = teacher['teacherId']
            return redirect(url_for('hello'))

        flash(error)
    
    return render_template('teacher/login.html')

@bp.route('/logout')
def logout():
    """Clear the current session, including the stored teacher id."""
    session.clear()
    return redirect(url_for('hello'))

