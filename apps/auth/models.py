from apps import login_manager
from flask_login import UserMixin
from apps import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import ValidationError
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True)
    username = db.Column(db.String(150), unique=True, index=True)
    password_hash = db.Column(db.String(150))
    confirmation_status = db.Column(db.Boolean, default=False)
    transaksi = db.relationship("Transaksi", backref="pemesanan", uselist=False)
    home_session = db.relationship("HomeSession", backref="home_session", uselist=False)
    wisata_session = db.relationship(
        "WisataSession", backref="wisata_session", uselist=True
    )
    belanja_user = db.relationship("BelanjaUser", backref="belanjaan", uselist=False)
    favorit_user = db.relationship("Favorit", backref="homestay_favorit", uselist=True)
    history_belanja = db.relationship(
        "Historybelanja", backref="history_user_berbelanja", uselist=False
    )
    user_detail = db.relationship("UserDetail", backref="detail_user", uselist=False)
    foto_user = db.Column(db.String(250))

    # This connects BlogPosts to a User Author.
    # posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password, foto_user):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.foto_user = foto_user

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


class UserDetail(db.Model):
    __tablename__ = "userdetail"
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    nama_lengkap = db.Column(db.String(100))
    jenis_kelamin = db.Column(db.String(20))
    nomor_hp = db.Column(db.String(100))
    alamat = db.Column(db.TEXT)
    foto_user_detail = db.Column(db.String(100))


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
