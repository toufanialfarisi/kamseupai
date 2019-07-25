from flask import Flask, render_template, redirect, url_for
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
file_path = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.join(file_path, "data.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir

app.config["SECRET_KEY"] = "KAMseupai291195"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

# from apps.auth import models
# from apps.home import models

# db.create_all()


from apps.auth.views import auth
from apps.home.views import home

app.register_blueprint(auth)
app.register_blueprint(home)
