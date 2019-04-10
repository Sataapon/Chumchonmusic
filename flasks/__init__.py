import os
from flask import Flask, render_template, g

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # homepage
    @app.route("/")
    def index():
        return render_template('index.html')

    # register the database and admin
    from . import db, admin
    db.init_app(app)
    admin.init_app(app)

    # apply the blueprints to the app
    from . import student, teacher, course
    app.register_blueprint(admin.bp)
    app.register_blueprint(student.bp)
    app.register_blueprint(teacher.bp)
    app.register_blueprint(course.bp)

    return app
