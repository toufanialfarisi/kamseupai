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

Migrate(app, db)
CORS(app)


from apps.auth.views import auth
from apps.home.views import home
from apps.auth_admin.views import admin
from apps.error_pages.handlers import error_pages

app.register_blueprint(auth)
app.register_blueprint(home)
app.register_blueprint(admin)
app.register_blueprint(error_pages)
