from flask_login import (
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required,
    LoginManager,
)
from flask import redirect, url_for, flash, render_template, request, Blueprint, session
from apps.auth import forms, models
from apps import db, email_confirm, Message, mail
from apps.auth.models import User, UserDetail
from apps.home.utility import host_mode, host
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
import random


auth = Blueprint("auth", __name__, template_folder="templates/")

google_blueprint = make_google_blueprint(
    scope=["profile", "email"],
    client_id="1010640175796-vnp220hj8ceepbniguvrvifju99bi398.apps.googleusercontent.com",
    client_secret="5VBRMSPo32XiuL4N5h481zqJ",
)


@auth.route("/google")
def google_auth_login():
    # cek apakah user authorized, klo tidak maka redirect ke google.login auth
    if not google.authorized:
        return redirect(url_for("google.login"))

    respon = google.get("/oauth2/v1/userinfo")
    respon_json = respon.json()
    return redirect(url_for("home.index"))


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):

    respon = blueprint.session.get("/oauth2/v2/userinfo")

    if respon.ok:
        respon_json = respon.json()
        email = respon_json["email"]
        username = respon_json["given_name"]
        password = str(respon_json["given_name"]) + "_" + str(random.randint(1, 1000))
        foto_user = respon_json["picture"]
        query = User.query.filter_by(email=email)
        try:
            user = query.one()
        except NoResultFound:
            user = User(
                email=email, username=username, password=password, foto_user=foto_user
            )
            db.session.add(user)
            db.session.commit()
        login_user(user)


@auth.route("/confirmation/<token>")
def confirmation(token):
    try:
        user_unconfirm = session["unconfirmed_user"]
        print(user_unconfirm)
        email = email_confirm.loads(token, salt="email-confirm")
        user_now = models.User.query.filter_by(username=user_unconfirm).first()
        user_now.confirmation_status = True
        models.db.session.add(user_now)
        models.db.session.commit()
        session.pop("unconfirmed_user", None)
        print("session terhapus")
    except:
        return render_template("expired.html")

    print("Token bekerja")
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["POST", "GET", "PUT" "DELETE"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    else:
        form = forms.RegisterForm()
        if form.validate_on_submit():
            user = models.User(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
                foto_user= host() + "/static/default_profile.png",
            )

            db.session.add(user)
            db.session.commit()

            session["unconfirmed_user"] = form.username.data
            get_user_id = User.query.filter_by(username=form.username.data).first().id
            user_detail = models.UserDetail(id_user=get_user_id)
            db.session.add(user_detail)
            db.session.commit()

            """
                token = email_confirm.dumps(email, salt="email-confirm")
                msg = Message(
                    "Konfirmasi Akun",
                    sender="kamseupai@makeitation.com",
                    recipients=[email],
                )
                link = url_for("auth.confirmation", token=token, external=True)

                host_server = host()
                msg.html = "<html>Silahkan konfirmasi akun Anda dengan mengklik link di bawah ini : <br> <strong> <a href='{}{}'> KONFIRMASI </a> </strong></html>".format(
                    host_server, link
                )
                mail.send(msg)
                return render_template("confirmation.html")
            """

            return redirect(url_for("auth.login"))
        return render_template("register.html", form=form)


@auth.route("/login", methods=["POST", "GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    else:

        form = forms.LoginForm()

        if form.validate_on_submit() and request.method == "POST":
            user = User.query.filter_by(username=form.username.data).first()
            try:
                check_user_confirmed = user.confirmation_status
                if user.check_password(form.password.data) and user is not None:
                    login_user(user)
                    next = request.args.get("next")
                    if next == None or not next[0] == "/":
                        next = url_for("home.index")
                    return redirect(next)
                else:
                    flash("Username / password Anda salah", "danger")
                    return redirect(url_for("auth.login"))

            except AttributeError:
                flash("Akun anda tidak terdaftar, silahkan register dulu !", "danger")
                return redirect(url_for("auth.login"))
        return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    try:
        token = google_blueprint.token["access_token"]
        resp = google.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": token},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert resp.ok, resp.text
        logout_user()  # Delete Flask-Login's session cookie
        del google_blueprint.token  # Delete OAuth token from storage
        return redirect(url_for("home.index"))
    except:
        logout_user()
        return redirect(url_for("home.index"))

