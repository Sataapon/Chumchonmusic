import functools, click

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash

from flasks.db import get_db

def init_admin():
    """Create admin"""
    db = get_db()

    admin = ('admin', generate_password_hash('123456'), 'admin')
    db.execute(
        'INSERT INTO Admin (Username, Password, Name) VALUES (?, ?, ?)', admin)
    db.commit()

@click.command('init-admin')
@with_appcontext
def init_admin_command():
    """Create command to initialized admin."""
    init_admin()
    click.echo('Initialized admin.')

def init_app(app):
    """Register admin functions with the Flask app. This is called by
    the appliciation factory.
    """
    app.cli.add_command(init_admin_command)

bp = Blueprint('admin', __name__, url_prefix='/admin')

def login_required(view):
    """View decorator that redirects anonymous admins to the login pages."""
    @functools.wrapgs(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for('admin.login'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_admin():
    """If a admin id is stored in the session, load the admin object from
    the database into ''g.admin''."""
    admin_id = session.get('admin_id')

    if admin_id is None:
        g.admin = None
    else:
        g.admin = get_db().execute(
            'SELECT * FROM Admin WHERE AdminId = ?', (admin_id,)
        ).fetchone()

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a admin by adding the admin id to the session."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        admin = db.execute(
            'SELECT * FROM Admin WHERE Username = ?', (username,)
        ).fetchone()

        if admin is None:
            error = 'Incorrect username.'
        elif not check_password_hash(admin['Password'], password):
            error = 'Incorrect password.'

        if error is None:
            # store the admin id in a new session and return to the index
            session.clear()
            session['admin_id'] = admin['AdminId']
            return redirect(url_for('index'))

        flash(error)
    
    return render_template('admin/login.html')

@bp.route('/logout')
def logout():
    """Clear the current session, including the stored student id."""
    session.clear()
    return redirect(url_for('index'))

@bp.route('/students')
def students():
    db = get_db()
    students = db.execute(
        'SELECT StudentId, Firstname, Lastname, Nickname FROM Student'
    ).fetchall()
    return render_template('admin/students.html', students=students)

@bp.route('/teachers')
def teachers():
    db = get_db()
    teachers = db.execute(
        'SELECT TeacherId, Firstname, Lastname, Nickname FROM Teacher'
    ).fetchall()
    return render_template('admin/teachers.html', teachers=teachers)

@bp.route('/courses')
def courses():
    db = get_db()
    courses = db.execute(
        'SELECT CourseId, Name FROM Course'
    ).fetchall()
    return render_template('admin/courses.html', courses=courses)

@bp.route('/course/create')
def course_create():
    return render_template('admin/course_create.html')
