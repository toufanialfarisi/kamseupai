from apps import login_manager
from flask_login import UserMixin
from apps import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import ValidationError


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(
        db.String(20), nullable=False, default="default_profile.png"
    )
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    transaksi = db.relationship("Transaksi", backref="pemesanan", uselist=False)
    home_session = db.relationship("HomeSession", backref="home_session", uselist=False)
    wisata_session = db.relationship(
        "WisataSession", backref="wisata_session", uselist=True
    )
    belanja_user = db.relationship("BelanjaUser", backref="belanjaan", uselist=False)
    favorit_user = db.relationship("Favorit", backref="homestay_favorit", uselist=True)

    # This connects BlogPosts to a User Author.
    # posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash, password)

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered already!")

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Sorry, that username is taken!")

    def __repr__(self):
        return f"UserName: {self.username}"

