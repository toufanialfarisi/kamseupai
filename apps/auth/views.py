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
    scope=["profile", "email"], redirect_url="{}".format(host() + "/google-auth")
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


@auth.route("/google-auth", methods=["POST", "GET"])
def google_auth():
    """
    menambahkan google auth pada aplikasi kamseupai. jadi user bisa 
    registrasi ataupun log in dengan menggunakan akun googlenya masing
    masing. hal ini akan menjadi lebih mudah
    """
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v1/userinfo")
    email = str(resp.json()["email"])
    username = str(resp.json()["name"])
    password = str(resp.json()["id"]) + str(resp.json()["family_name"])
    user_picture = str(resp.json()["picture"])
    user_google_id = str(resp.json()["id"])
    session["user_id"] = user_google_id
    """
    cek terlebih dahulu apakah user email pada google auth sudah didaftarkan atau belum.
    jika sudah ada, maka hanya login biasa tanpa melakukan penulisan data ke dalam db. jika
    belum ada, maka ambil data / info dari google auth lalu tulis ke dalam db.
    """
    if resp.json()["email"] in [data.email for data in models.User.query.all()]:
        print("email google sudah ada dan siap untuk login")
        user = models.User.query.filter_by(username=username).first()
        # memasukan foto profile dari api google auth dengan membuat session
        session["user_picture"] = user_picture
        login_user(user)  # masukan user ke dalam login manager nya
        next = request.args.get("next")
        if next == None or not next[0] == "/":
            next = url_for("home.index")
        return redirect(next)
    else:
        print("email google tidak tersedia, sehingga regist automatis")
        print(resp.json())
        # assert resp.ok, resp.text
        session["user_picture"] = user_picture
        user_google = models.User(email=email, username=username, password=password)
        models.db.session.add(user_google)
        models.db.session.commit()
        user_detail = models.UserDetail(
            id_user=user_google_id, foto_user=session["user_picture"]
        )
        models.db.session.add(user_detail)
        models.db.session.commit()
        user = models.User.query.filter_by(username=username).first()

        login_user(user)
        next = request.args.get("next")
        if next == None or not next[0] == "/":
            next = url_for("home.index")
        return redirect(next)
    # return "email {}, username {}, password {}".format(email, username, password)

    # return "berhasil login dengan google"

    # return "You are {email} on Google, here your detail login {user_info}".format(
    #     email=resp.json()["email"], user_info=resp.json()
    # )


# @auth.route("/google")
# def google_page():

# return "berhasil"


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

