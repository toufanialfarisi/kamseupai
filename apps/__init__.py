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
import os
import logging

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


app = Flask(__name__)
app.config.from_object(os.getenv("APP_SETTINGS"))

app.jinja_env.filters["zip"] = zip
db = SQLAlchemy(app)
file_path = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.join(file_path, "data.sqlite")


db_config = {
    "production": {
        "db_type": "postgresql",
        "username": "rqjlcbouwdptml",
        "password": "140d296ff6a2103213affa9eaeaa8b3f2d24cb15c1b9a321ce77277db35bca55",
        "host": "ec2-54-197-238-238.compute-1.amazonaws.com",
        "port": "5432",
        "database": "da3kp68t3m2lui",
    },
    "development": {
        "db_type": "mysql",
        "username": "kamseupai",
        "password": "kampungantapisukses",
        "host": "localhost",
        "port": "5432",
        "database": "monolitik",
    },
}

db_dev = os.getenv("HOST_MODE")
if db_dev == "development":
    app.config["SQLALCHEMY_DATABASE_URI"] = "{}://{}:{}@{}:{}/{}".format(
        db_config["development"]["db_type"],
        db_config["development"]["username"],
        db_config["development"]["password"],
        db_config["development"]["host"],
        db_config["development"]["port"],
        db_config["development"]["database"],
    )

elif db_dev == "production":

    app.config["SQLALCHEMY_DATABASE_URI"] = "{}://{}:{}@{}:{}/{}".format(
        db_config["production"]["db_type"],
        db_config["production"]["username"],
        db_config["production"]["password"],
        db_config["production"]["host"],
        db_config["production"]["port"],
        db_config["production"]["database"],
    )

    # app.config[
    #     "SQLALCHEMY_DATABASE_URI"
    # ] = "postgres://rqjlcbouwdptml:140d296ff6a2103213affa9eaeaa8b3f2d24cb15c1b9a321ce77277db35bca55@ec2-54-197-238-238.compute-1.amazonaws.com:5432/da3kp68t3m2lui"

    # app.config[
    #         "SQLALCHEMY_DATABASE_URI"
    #     ] = "psql://kamseupai:kampungantapisukses@localhost/monolitik"

else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir


app.config["SECRET_KEY"] = "KAMseupai291195"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# @app.before_request
# def before_request():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(minutes=1)

# Note
# ===========================================================
print(" * DATABASE MODE : {}".format(db_dev))
print(" * CONFIG_MODE : {}".format(os.environ.get("APP_SETTINGS")))
# ===========================================================

app.config.from_pyfile("config.cfg")
email_confirm = URLSafeTimedSerializer("KAMseupai291195")
mail = Mail(app)

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
