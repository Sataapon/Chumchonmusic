import functools

from flask import (
    Blueprint,g, redirect, render_template, request, url_for
)
from flasks.db import get_db

bp = Blueprint('course', __name__, url_prefix='/course')

@bp.route('/')
def index():
    db = get_db()
    courses = db.execute('SELECT Course.Name as CouName, Instrument.Name as InsName, Teacher.Nickname, Teacher.FirstName, Teacher.Lastname \
            FROM Course JOIN Instrument ON Instrument.InstrumentId = Course.InstrumentId \
            JOIN Teach ON Course.CourseId = Teach.CourseId \
            JOIN Teacher ON Teacher.TeacherId = Teach.TeacherId').fetchall()

    return render_template('course/courses.html', courses=courses)


