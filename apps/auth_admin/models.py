from apps import login_manager
from apps import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import ValidationError


class Admin(db.Model):

    # Create a table in the db
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(
        db.String(20), nullable=False, default="default_profile.png"
    )
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash, password)

    def validate_email(self, field):
        # Check if not None for that user email!
        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered already!")

    def validate_username(self, field):
        # Check if not None for that username!
        if Admin.query.filter_by(username=field.data).first():
            raise ValidationError("Sorry, that username is taken!")

    def __repr__(self):
        return f"UserName: {self.username}"

