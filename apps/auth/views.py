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
from apps.auth.models import User
from apps.home.utility import host_mode, host

auth = Blueprint("auth", __name__, template_folder="templates/")


@auth.route("/confirmation/<token>")
def confirmation(token):
    try:
        user_unconfirm = session["unconfirmed_user"]
        email = email_confirm.loads(token, salt="email-confirm")
        user_now = models.User.query.filter_by(username=user_unconfirm).first()
        user_now.confirmation_status = True
        models.db.session.add(user_now)
        models.db.session.commit()
    except:
        return render_template("expired.html")

    print("Token bekerja")
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["POST", "GET", "PUT" "DELETE"])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        user = models.User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()

        session["unconfirmed_user"] = form.username.data

        email = form.email.data
        token = email_confirm.dumps(email, salt="email-confirm")
        msg = Message(
            "Konfirmasi Akun", sender="kamseupai@makeitation.com", recipients=[email]
        )
        link = url_for("auth.confirmation", token=token, external=True)

        host_server = host()
        msg.html = "<html>Silahkan konfirmasi Akun  anda dengan mengklik link di bawah ini : <br> <strong> <a href='{}{}'> KONFIRMASI </a> </strong></html>".format(
            host_server, link
        )
        mail.send(msg)
        return render_template("confirmation.html")
    return render_template("register.html", form=form)


@auth.route("/login", methods=["POST", "GET"])
def login():

    # if current_user.is_authenticated:
    #     return redirect(url_for("register"))

    form = forms.LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        check_user_confirmed = user.confirmation_status
        try:
            if (
                user.check_password(form.password.data)
                and user is not None
                and check_user_confirmed is True
            ):
                # if check_password_hash(user.password, form.password.data) and user is
                login_user(user)
                next = request.args.get("next")
                if next == None or not next[0] == "/":
                    next = url_for("home.index")
                return redirect(next)
        except:
            flash("wrong password or username", "danger")
            return redirect(url_for("auth.login"))
    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
