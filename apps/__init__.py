from flask import Flask, render_template, redirect, url_for, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_cors import CORS
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail, Message
from datetime import timedelta
from flask_cors import CORS
import os
import logging

# HANDLING WARNING IN TERMINAL
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

# ================================================
# APP CONFIGURATION
app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
app.jinja_env.filters["zip"] = zip
db = SQLAlchemy(app)  # DATABASE SQLALCHEMY
CORS(app)  # HEADER ALLOW ORIGIN ALL
Migrate(app, db)  # DATABASE MIGRATION

# EMAIL PURPOSE
email_confirm = URLSafeTimedSerializer("KAMseupai291195")
mail = Mail(app)

# Login session timeout
# @app.before_request
# def before_request():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(minutes=1)

# COMMAND MANAGER TO TRIGGER PYTHON MANAGE.PY RUNSERVER/SHELL/DB
manager = Manager(app)
manager.add_command("db", MigrateCommand)

# LOGIN CONFIGURATION PURPOSE
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


# BLUEPRINT CONFIGURATION PURPOSE
from apps.auth.views import auth, google_blueprint
from apps.home.views import home
from apps.auth_admin.views import admin
from apps.error_pages.handlers import error_pages


app.register_blueprint(google_blueprint, url_prefix="/google_login")
app.register_blueprint(auth)
app.register_blueprint(home)
app.register_blueprint(admin)
app.register_blueprint(error_pages)
