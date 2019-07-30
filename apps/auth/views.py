from flask_login import (
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required,
    LoginManager,
)
from flask import redirect, url_for, flash, render_template, request, Blueprint
from apps.auth import forms, models
from apps import db
from apps.auth.models import User


auth = Blueprint("auth", __name__, template_folder="templates/")


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
        flash("Thanks for registration", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth.route("/login", methods=["POST", "GET"])
def login():

    # if current_user.is_authenticated:
    #     return redirect(url_for("register"))

    form = forms.LoginForm()

    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        try:
            if user.check_password(form.password.data) and user is not None:
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
