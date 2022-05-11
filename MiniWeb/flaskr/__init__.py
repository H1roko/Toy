import os

from flask import Flask
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from datetime import timedelta


def create_app(test_config=None):
    # 创建并配置APP
    app = Flask(__name__, instance_relative_config=True)
    app.send_file_max_age_default = timedelta(seconds=1)
    app.config.from_mapping(
        SECRET_KEY='dev',
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

    @app.route('/')
    def index():
        """Show all the posts, most recent first."""
        from . import db
        db = db.get_db()
        passages = db.execute(
            "SELECT p.id, title, body, author_id, name"
            " FROM passage p JOIN author a ON p.author_id = a.id"
            " ORDER BY p.id DESC").fetchmany(4)
        return render_template("index.html",
                               passages=passages,
                               content="你想找什么？")

    @app.route('/search', methods=("GET", "POST"))
    def search():
        content = request.values.get('content')
        if content != '':
            from . import db
            db = db.get_db()
            results = db.execute(
                " SELECT p.id, title, body, author_id, name"
                " FROM passage p JOIN author a ON p.author_id = a.id"
                " WHERE title LIKE '%" + f"{content}" + "%'"
                " UNION"
                " SELECT p.id, title, body, author_id, name"
                " FROM passage p JOIN author a ON p.author_id = a.id"
                " WHERE name LIKE '%" + f"{content}" + "%'").fetchall()
            return render_template("index.html",
                                   passages=results,
                                   content=content)
        else:
            from . import db
            db = db.get_db()
            passages = db.execute(
                "SELECT p.id, title, body, author_id, name"
                " FROM passage p JOIN author a ON p.author_id = a.id"
                " ORDER BY p.id DESC").fetchmany(4)
            return render_template("index.html",
                                   passages=passages,
                                   content="你想找什么？")

    @app.route('/detail/<int:id>', methods=("GET", "POST"))
    def detail(id):
        from . import db
        db = db.get_db()
        detail = db.execute(
            "SELECT p.id, title, body, author_id, name"
            " FROM passage p JOIN author a ON p.author_id = a.id"
            " WHERE p.id = " + f"{id}").fetchone()
        return render_template('detail.html', detail=detail)

    from . import db
    db.init_app(app)

    return app