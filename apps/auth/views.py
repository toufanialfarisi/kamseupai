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
from flask_dance.contrib.google import make_google_blueprint, google


auth = Blueprint("auth", __name__, template_folder="templates/")
google_bp = make_google_blueprint(
    scope=["profile", "email"], redirect_url="{}".format(host() + "/google-auth-login")
)


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


@auth.route("/google-auth-login")
def google_auth_login():
    # cek apakah user authorized, klo tidak maka redirect ke google.login auth
    if not google.authorized:
        return redirect(url_for("google.login"))

    # ambil respon json google authnya jika sudah authentication
    respon = google.get("/oauth2/v1/userinfo")
    email = respon.json()["email"]
    username = respon.json()["name"]
    session["username"] = username
    password = respon.json()["family_name"]
    picture = respon.json()["picture"]
    user_google_id = respon.json()["id"]

    """ 
        jika pertama kali query write data, maka tulis/masukan data json google ke db 
        Ini yang disebut sebagai REGISTER
    """
    try:
        print("REGISTER")
        print("REGISTER")
        print("REGISTER")
        print("REGISTER")
        print("REGISTER")

        user = models.User(email, username, password)
        models.db.session.add(user)
        models.db.session.commit()

        user = models.User.query.filter_by(username=username).first()
        login_user(user)  # masukan user ke dalam login manager nya
        user_detail = models.UserDetail(id_user=user.id, foto_user=picture)
        models.db.session.add(user_detail)
        models.db.session.commit()
        next = request.args.get("next")
        if next == None or not next[0] == "/":
            next = url_for("home.index")
        return redirect(next)

    except:
        print("LOGIN")
        print("LOGIN")
        print("LOGIN")
        print("LOGIN")
        print("LOGIN")

        """ 
            jika sudah query / write data yg sama sebelumnya, 
            maka lakukan pass supaya tidak terjadi duplikasi. 
            ini yang disebut sebagai LOGIN
         """
        pass
    return redirect(url_for("home.index"))


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
            )

            db.session.add(user)
            db.session.commit()

            session["unconfirmed_user"] = form.username.data
            get_user_id = User.query.filter_by(username=form.username.data).first().id
            user_detail = models.UserDetail(id_user=get_user_id)
            db.session.add(user_detail)
            db.session.commit()

            email = form.email.data
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
                if (
                    user.check_password(form.password.data)
                    and user is not None
                    and check_user_confirmed is True
                ):

                    login_user(user)
                    next = request.args.get("next")
                    if next == None or not next[0] == "/":
                        next = url_for("home.index")
                    return redirect(next)
                elif (
                    user.check_password(form.password.data)
                    and user is not None
                    and check_user_confirmed is False
                ):
                    flash(
                        "Akun belum terkonfirmasi, silahkan cek email Anda !", "danger"
                    )
                    return redirect(url_for("auth.login"))
                else:
                    flash("Username / password Anda salah", "danger")
                    return redirect(url_for("auth.login"))

            except AttributeError:
                flash("Akun anda tidak terdaftar, silahkan register dulu !", "danger")
                return redirect(url_for("auth.login"))
        return render_template("login.html", form=form)


"""
SEMENTARA WAKTU, FITUR LOGOUT SAYA DISABLE DULU.
KARENA ADA LOGIC YANG BELUM TERSELESAIKAN

@auth.route("/logout")
def logout():

    token = google_bp.token["access_token"]
    try:
        print("token expired")
        logout_user()
        return redirect(url_for("auth.login"))
    except:
        print("token belum expired")
        if token is not None:
            resp = google.post(
                "https://accounts.google.com/o/oauth2/revoke",
                params={"token": token},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            assert resp.ok, resp.text
            logout_user()
            del google_bp.token
            print("ada token google auth nya")
            return redirect(url_for("auth.login"))
        else:
            logout_user()
            print("tidak ada token google auth nya")
            return redirect(url_for("auth.login"))

"""
