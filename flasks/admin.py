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

def init_instruments():
    """Create instruments"""
    db = get_db()

    instruments = [('Guitar',), ('Paino',), ('Drums',)]
    db.executemany(
        'INSERT INTO Instrument (Name) VALUES (?)', instruments)
    db.commit()

@click.command('init-instruments')
@with_appcontext
def init_instruments_command():
    """Create command to initialized instruments."""
    init_instruments()
    click.echo('Initialized instruments.')

def init_app(app):
    """Register admin functions with the Flask app. This is called by
    the appliciation factory.
    """
    app.cli.add_command(init_admin_command)
    app.cli.add_command(init_instruments_command)
    
bp = Blueprint('admin', __name__, url_prefix='/admin')

def login_required(view):
    """View decorator that redirects anonymous admins to the login pages."""
    @functools.wraps(view)
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
@login_required
def students():
    db = get_db()
    rows = db.execute('select * from Student').fetchall()
    return render_template('admin/students.html', datas=rows)

@bp.route('/teachers')
@login_required
def teachers():
    db = get_db()
    rows = db.execute('select * from Teacher').fetchall()
    return render_template('admin/teachers.html', datas=rows)

@bp.route('/courses')
@login_required
def courses():
    db = get_db()
    course_list = db.execute(
        'select instrument.name, Course.name as level, Course.price, teacher.Nickname, Course.HousPerTime, Course.NumOfTime from Course\
                    left join Instrument on Instrument.InstrumentId = Course.InstrumentId\
                        join Teach on Teach.CourseId = Course.CourseId\
                            join Teacher on Teacher.TeacherId = teach.TeacherId'
    ).fetchall()
    return render_template('admin/courses.html', datas= course_list)

@bp.route('/course/create', methods=('GET', 'POST'))
@login_required
def create_course():
    db = get_db()
    if request.method == 'POST':
        values = ()
        for key in request.form:
            if key == 'instrument':
                values += (int(db.execute('SELECT InstrumentId FROM Instrument WHERE Name = ?',(request.form[key],)).fetchone()['InstrumentId']),)
            elif key == 'price' or key == 'houspertime' or key == 'numoftimes':
                values += (int(request.form[key]),)
            else:
                values += (request.form[key],)
        db.execute('INSERT INTO Course (Name, Price, HousPerTime, NumOfTimes, InstrumentId) VALUES (?, ?, ?, ?, ?)', values)
        db.commit()

        return redirect(url_for('index'))

    instruments = db.execute('SELECT Name FROM Instrument').fetchall()
    return render_template('admin/course/create.html', instruments=instruments)

