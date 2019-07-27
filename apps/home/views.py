from flask import redirect, url_for, flash, render_template, request, Blueprint, session
from apps.home import forms, models
from apps.utils import validasi_type, upload_file
from apps.config import IMAGES_DIR, MY_IP
from flask_login import current_user, login_required, logout_user
import random
import string

home = Blueprint("home", __name__, template_folder="templates/")


def custom_session_idhomestay(homestay_id):
    id_homestay = models.Homestay.query.get(homestay_id)
    return id_homestay


def show_fav():
    fav = models.Favorit.query.all()
    if fav:
        is_fav_exist = True
    else:
        is_fav_exist = False
    return (fav, is_fav_exist)


@home.route("/", methods=["GET"])
def index():
    model = models.Homestay.query.all()
    fav, is_fav_exist = show_fav()
    return render_template("home.html", form=model, favs=fav, favs_exist=is_fav_exist)


@home.route("/favorit/<int:id>", methods=["GET"])
@login_required
def favorit(id):
    user_now = current_user.get_id()
    model_homestay = models.Homestay.query.get(id)
    fav = models.Favorit(fav_homestay=model_homestay.nama_homestay, id_user=user_now)
    models.db.session.add(fav)
    models.db.session.commit()
    return redirect(url_for("home.index"))


@home.route("/homestay/<int:id>", methods=["GET", "POST"])
def detail_homestay(id):
    model = models.Homestay.query.get(id)
    fav, is_fav_exist = show_fav()
    if request.method == "POST":
        session["malam"] = request.form["malam"]
        return redirect(url_for("home.book_homestay", id=id))
    return render_template(
        "home_detail.html", form=model, favs=fav, favs_exist=is_fav_exist
    )


@home.route("/book/homestay/<int:id>", methods=["GET", "POST"])
@login_required
def book_homestay(id):
    model = models.Homestay.query.get(id)
    session["save_id_homestay"] = id
    print(
        "homestay booked, saya simpen id_homestay-nya = ", session["save_id_homestay"]
    )
    fav, is_fav_exist = show_fav()
    save_id_homestay = models.HomeSession(
        id_homestay=id, user_now=current_user.get_id()
    )
    models.db.session.add(save_id_homestay)
    models.db.session.commit()
    model_wisata = models.Wisata.query.all()
    return render_template(
        "book_wisata.html",
        form=model_wisata,
        form_homestay=model,
        favs=fav,
        favs_exist=is_fav_exist,
    )


@home.route("/book/homestay/wisata/<int:id>", methods=["GET"])
@login_required
def book_wisata(id):
    model = models.Wisata.query.get(id)
    session["save_id_wisata"] = id
    print("Wisata booked, saya simpen id_wisata-nya = ", session["save_id_wisata"])
    if request.method == "GET":
        return redirect(url_for("home.book_processing", id=id))


@home.route("/book-processing")
@login_required
def book_processing():
    id_homestay = session["save_id_homestay"]
    try:
        id_wisata = session["save_id_wisata"]
    except:
        id_wisata = session["save_id_wisata"] = None
    if id_wisata == None:
        return redirect(url_for("home.checkout"))
    else:
        user_now = current_user.get_id()
        checkout = models.Transaksi(
            id_homestay=id_homestay, id_wisata=id_wisata, id_user=user_now
        )
        models.db.session.add(checkout)
        models.db.session.commit()
        return redirect(url_for("home.checkout"))


@home.route("/book/homestay/wisata/checkout", methods=["GET"])
@login_required
def checkout():
    user_now = current_user.get_id()
    id_homestay = session["save_id_homestay"]
    n_malam = int(session["malam"])
    model_homestay = models.Homestay.query.get(id_homestay)
    """
    1. query all transaksinya
    2. filter transaksi berdasarkan id_user = 1
    3. ambil id_wisata dari filter transaksi tersebut
    4. iterasi list dari id_wisata 
    5. tampilkan di front html 
    """
    fav, is_fav_exist = show_fav()
    total_tagihan = []
    biaya_homestay = None
    biaya_wisata = []
    form_wisata = []

    paket_wisata = models.Transaksi.query.filter_by(id_homestay=id_homestay).all()

    for val in paket_wisata:
        show_wisata = models.Wisata.query.get(val.id_wisata)
        form_wisata.append(show_wisata)

    for val in form_wisata:
        biaya_wisata.append(val.biaya)

    biaya_wisata = sum(biaya_wisata)
    biaya_homestay = model_homestay.harga * n_malam
    total_biaya = biaya_wisata + biaya_homestay
    fav, is_fav_exist = show_fav()

    return render_template(
        "checkout.html",
        form_homestay=model_homestay,
        form_wisata=form_wisata,
        total=total_biaya,
        malam=n_malam,
        favs=fav,
        favs_exist=is_fav_exist,
    )


@home.route("/pay", methods=["GET"])
@login_required
def pay():
    user_now = current_user.get_id()
    id_homestay = session["save_id_homestay"]
    n_malam = int(session["malam"])
    model_homestay = models.Homestay.query.get(id_homestay)

    biaya_wisata = []
    form_wisata = []

    paket_wisata = models.Transaksi.query.filter_by(id_user=user_now).all()
    for val in paket_wisata:
        show_wisata = models.Wisata.query.get(val.id_wisata)
        form_wisata.append(show_wisata)

    for val in form_wisata:
        biaya_wisata.append(val.biaya)

    biaya_wisata = sum(biaya_wisata)
    biaya_homestay = model_homestay.harga * n_malam
    total_biaya = biaya_wisata + biaya_homestay
    fav, is_fav_exist = show_fav()
    return render_template(
        "pay.html", total=total_biaya, favs=fav, favs_exist=is_fav_exist
    )


@home.route("/pay/confirmed", methods=["GET"])
@login_required
def pay_confirmed():
    session.pop("save_id_homestay", None)
    session.pop("save_id_wisata", None)
    session.pop("malam", None)
    trans = models.Transaksi.query.all()
    for data in trans:
        models.db.session.delete(data)
        models.db.session.commit()
    print("done")
    fav, is_fav_exist = show_fav()
    return render_template("pay_confirmed.html", favs=fav, favs_exist=is_fav_exist)


def code_homestay(stringLength=6, gen_for="H"):
    """Generate a random string of letters and digits """
    lettersAndDigits = gen_for + string.ascii_letters + string.digits
    return "".join(random.choice(lettersAndDigits) for i in range(stringLength))


@home.route("/homestay/add", methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def add_homestay():
    form = forms.HomestayForm()
    fav, is_fav_exist = show_fav()
    if form.validate_on_submit() and request.method == "POST":
        file = request.files["foto_homestay"]
        folder = IMAGES_DIR + "/homestay"
        foto = upload_file(file, folder)  # return random name
        foto = "http://localhost" + "/" + foto

        nama_homestay = validasi_type(form.nama_homestay.data, str)
        alamat = validasi_type(form.alamat.data, str)
        deskripsi = validasi_type(form.deskripsi.data, str)
        fasilitas = validasi_type(form.fasilitas.data, str)
        harga = validasi_type(form.harga.data, int)

        model = models.Homestay(
            code_homestay=code_homestay(stringLength=5, gen_for="H"),
            nama_homestay=nama_homestay,
            alamat=alamat,
            deskripsi=deskripsi,
            fasilitas=fasilitas,
            harga=harga,
            foto_homestay=foto,
        )
        models.db.session.add(model)
        models.db.session.commit()
        flash("Homestay berhasil ditambah", "success")
        return redirect(url_for("home.add_homestay"))
    return render_template(
        "add_homestay.html", form=form, favs=fav, favs_exist=is_fav_exist
    )


@home.route("/homestay/wisata/add", methods=["GET", "POST", "PUT", "DELETE"])
@login_required
def add_wisata():
    form = forms.WisataForm()
    fav, is_fav_exist = show_fav()
    if request.method == "POST":
        file = request.files["foto_wisata"]
        # print(file)
        # return "test"
        folder = IMAGES_DIR + "/wisata"
        foto = upload_file(file, folder)  # return random name
        foto = "http://localhost" + "/" + foto

        wisata = validasi_type(form.wisata.data, str)
        fasilitas = validasi_type(form.fasilitas.data, str)
        biaya = validasi_type(form.biaya.data, str)
        kegiatan = validasi_type(form.biaya.data, int)
        id_homestay = validasi_type(form.id_homestay.data, int)

        model = models.Wisata(
            code_wisata=code_homestay(stringLength=5, gen_for="W"),
            wisata=wisata,
            fasilitas=fasilitas,
            biaya=biaya,
            kegiatan=kegiatan,
            id_homestay=id_homestay,
            foto_wisata = foto,
        )
        models.db.session.add(model)
        models.db.session.commit()
        flash("Wisata berhasil ditambah", "success")
        return redirect(url_for("home.add_wisata"))
    return render_template(
        "add_wisata.html", form=form, favs=fav, favs_exist=is_fav_exist
    )


@home.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

