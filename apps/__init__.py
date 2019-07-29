from flask import Flask, render_template, redirect, url_for
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_cors import CORS
import os

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.jinja_env.filters["zip"] = zip
db = SQLAlchemy(app)
file_path = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.join(file_path, "data.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir
app.config["SECRET_KEY"] = "KAMseupai291195"


manager = Manager(app)
manager.add_command("db", MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@manager.command
def show_urls():
    import urllib

    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ",".join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote(
            "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
        )
        output.append(line)
    for line in sorted(output):
        print(line)


Migrate(app, db)
CORS(app)

# from apps.auth import models
# from apps.home import models

# db.create_all()


from apps.auth.views import auth
from apps.home.views import home

app.register_blueprint(auth)
app.register_blueprint(home)
