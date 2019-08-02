from flask import redirect, url_for, flash, render_template, request, Blueprint, session
from apps.home.forms import * 
from apps.home.models import * 
from apps.utils import validasi_type, upload_file
from apps.config import IMAGES_DIR, MY_IP
from flask_login import current_user, login_required, logout_user
import random
import string
from datetime import date, time, datetime
from apps.home.utility import * 

home = Blueprint("home", __name__, template_folder="templates/")


@home.route("/clear-session", methods=["GET", "POST"])
def delete_sessions():
    trans = models.Transaksi.query.all()
    for data in trans:
        models.db.session.delete(data)
        models.db.session.commit()

    session.pop("id_save_homestay", None)
    session.pop("id_save_wisata", None)
    session.pop("malam", None)
    session.pop("check_in", None)
    session.pop("check_out", None)
    session.pop("ci", None)
    session.pop("co", None)
    session.pop("total_biaya", None)
    return 'all sessions are clear'



@home.route("/", methods=["GET", "POST"])
def index():
    ls_curency = []
    model = models.Homestay.query.all()
    fav, is_fav_exist = show_fav()
    ls_diskon = []
    for cur in model:
        rupiah = formatrupiah(cur.harga)
        ls_curency.append(rupiah)
        real_harga = cur.harga 
        potongan_harga = cur.harga * (cur.diskon/100)
        disk = int(real_harga - potongan_harga)
        thediskon = formatrupiah(disk)
        ls_diskon.append(thediskon)
    
    searchform = searchForm()
    if searchform.validate_on_submit():
        post = Homestay.query.filter(Homestay.nama_homestay.like('%' + searchform.keyword.data + '%'))
        post = post.order_by(Homestay.nama_homestay).all()
        
        return render_template(
            "home.html", 
            formm=searchform,
            form=post, 
            favs=fav, 
            favs_exist=is_fav_exist, 
            rupiah=ls_curency, 
            ls_diskon=ls_diskon,
            host=host(),
        )

    return render_template(
        "home.html", 
        formm=searchform,
        form=model, 
        favs=fav, 
        favs_exist=is_fav_exist, 
        rupiah=ls_curency, 
        ls_diskon=ls_diskon,
        host=host(),
        )


@home.route("/favorit/<int:id>", methods=["GET"])
@login_required
def favorit(id):
    user_now = current_user.get_id()
    model_homestay = models.Homestay.query.get(id)
    fav = models.Favorit(fav_homestay=model_homestay.nama_homestay, id_user=user_now)
    models.db.session.add(fav)
    models.db.session.commit()
    return redirect(url_for("home.index"))

@home.route("/checkout/favorit/<int:id>", methods=["GET"])
@login_required
def checkout_favorit(id):
    user_now = current_user.get_id()
    model_homestay = models.Homestay.query.get(id)
    fav = models.Favorit(fav_homestay=model_homestay.nama_homestay, id_user=user_now)
    models.db.session.add(fav)
    models.db.session.commit()
    return redirect(url_for("home.checkout"))

@home.route("/remove/item/<int:id>", methods=["GET"])
@login_required
def remove_item(id):
    user_now = current_user.get_id()
    session.pop('save_id_homestay', None)
    return redirect(url_for("home.remove_item_notif"))

@home.route("/remove/item/notif", methods=["GET"])
@login_required
def remove_item_notif():
    flash("Item Berhasil dihapus","success")
    return render_template("checkout_notif.html")

@home.route("/remove/item/paket/<int:id>", methods=["GET"])
@login_required
def remove_paket(id):
    user_now = current_user.get_id()
    session.pop('save_id_wisata', None)
    transaksi = models.Transaksi.query.all()
    for data in transaksi:
        models.db.session.delete(data)
        models.db.session.commit()
    return redirect(url_for("home.checkout"))

from datetime import datetime



@home.route("/homestay/<int:id>", methods=["GET", "POST"])
def detail_homestay(id):
    cur = models.Homestay.query.get(id)

    fav, is_fav_exist = show_fav()
    ls_diskon = []
    rupiah = formatrupiah(cur.harga)
    real_harga = cur.harga 
    potongan_harga = cur.harga * (cur.diskon/100)
    disk = int(real_harga - potongan_harga)
    thediskon = formatrupiah(disk)
    fav, is_fav_exist = show_fav()
    model_wisata = models.Wisata.query.filter_by(id_homestay=id).all()
    print(model_wisata)
    if request.method == "POST":

        if request.form["malam"] and request.form["kamar"] and request.form["malam"] and request.form["check_in"]:

            malam = session["malam"] = request.form["malam"]
            tgl_checkin = request.form["check_in"] # session["check_in"] = 
            checkin = tgl_checkin.split('-')
            check_in = checkin[0] + '-' + checkin[1] +'-' + checkin[2]
            session["ci"] = datetime(int(checkin[0]), int(checkin[1]), int(checkin[2]))
            tgl_checkin = session["check_in"] = check_in
            

            kamar = session["kamar"] = request.form["kamar"]
            checkout = tgl_checkin.split('-')
            # tgl_checkout = int(checkout[2]) + int(malam)

            '''
            checkin[0] = tahun
            checkin[1] = bulan
            checkin[2] = tanggal 
            '''

            try:
                tgl_checkout, bulan = tanggal_checkout(int(malam), int(checkin[2]), int(checkin[1]))
                check_out = session["check_out"] = checkout[0] + '-' + str(bulan) + '-' +  str(tgl_checkout)  
                session["co"] = datetime(int(checkout[0]), int(bulan), int(tgl_checkout))      
            except:
                tgl_checkout = tanggal_checkout(int(malam), int(checkin[2]), int(checkin[1]))        
                check_out = session["check_out"] = checkout[0] + '-' + str(checkout[1]) + '-' +  str(tgl_checkout)        
                session["co"] = datetime(int(checkout[0]), int(checkout[1]), int(tgl_checkout))
            
            return redirect(url_for("home.book_homestay", id=id))
        else:
            flash("Silahkan isi semua form di bawah ini", "danger")
            redirect(url_for("home.detail_homestay", id=id))

    
    return render_template(
        "home_detail.html", 
        form=cur, 
        favs=fav, 
        favs_exist=is_fav_exist, 
        host=host(),
        formatrupiah=formatrupiah,
        diskon=thediskon, 
        form_wisata=model_wisata,
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
    model_wisata = models.Wisata.query.filter_by(id_homestay=id).all()
    return render_template(
        "book_wisata.html",
        form=model_wisata,
        form_homestay=model,
        favs=fav,
        favs_exist=is_fav_exist,
        host=host(),
        formatrupiah=formatrupiah,
    )


@home.route("/book/homestay/wisata/<int:id>", methods=["GET"])
@login_required
def book_wisata(id):
    session["save_id_wisata"] = id
    print("/book/homestay/wisata/<int:id> == >",session["save_id_wisata"])
    print("Wisata booked, saya simpen id_wisata-nya = ", session["save_id_wisata"])    
    return redirect(url_for("home.book_processing", id=id))


@home.route("/book-processing")
@login_required
def book_processing():

    id_homestay = session["save_id_homestay"]
    malam = session["malam"]
    kamar = session["kamar"]
    tgl_check_in = session["check_in"]
    tgl_check_out = session["check_out"]

    try:
        id_wisata = session["save_id_wisata"]
    except:
        id_wisata = session["save_id_wisata"] = None
        
    if id_wisata == None:
        return redirect(url_for("home.checkout"))

    else:
        user_now = current_user.get_id()
        checkout = models.Transaksi(
            id_homestay=id_homestay, 
            id_wisata=id_wisata, 
            id_user=user_now,
            malam=malam,
            kamar=kamar,
            tgl_check_in=tgl_check_in,
            tgl_check_out=tgl_check_out
        )

        models.db.session.add(checkout)
        models.db.session.commit()
        return redirect(url_for("home.checkout"))


@home.route("/book/homestay/wisata/checkout", methods=["GET"])
@login_required
def checkout():
    user_now = current_user.get_id()
    id_homestay = session["save_id_homestay"]
    tgl_check_in = session["check_in"]
    tgl_check_out = session["check_out"]
    print("check in ", tgl_check_in)
    try:
        n_malam = int(session["malam"])
    except:
        n_malam = 1
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
    
    rupiah = formatrupiah(model_homestay.harga)
    real_harga = model_homestay.harga 
    potongan_harga = model_homestay.harga * (model_homestay.diskon/100)
    disk = int(real_harga - potongan_harga)
    thediskon = formatrupiah(disk)

    biaya_wisata = sum(biaya_wisata)
    biaya_homestay = disk * n_malam
    total_biaya = biaya_wisata + biaya_homestay
    session["total_biaya"] = total_biaya
    fav, is_fav_exist = show_fav()

    return render_template(
        "checkout.html",
        form_homestay=model_homestay,
        form_wisata=form_wisata,
        total=total_biaya,
        malam=n_malam,
        favs=fav,
        favs_exist=is_fav_exist,
        formatrupiah=formatrupiah,
        host=host(),
        check_in=tgl_check_in,
        check_out=tgl_check_out,
        diskon=thediskon,
    )


@home.route("/pay", methods=["GET"])
@login_required
def pay():
    user_now = current_user.get_id()
    id_homestay = session["save_id_homestay"]
    try:
        n_malam = int(session["malam"])
    except:
        n_malam = 1
    model_homestay = models.Homestay.query.get(id_homestay)

    biaya_wisata = []
    form_wisata = []

    paket_wisata = models.Transaksi.query.filter_by(id_user=user_now).all()
    for val in paket_wisata:
        show_wisata = models.Wisata.query.get(val.id_wisata)
        form_wisata.append(show_wisata)

    for val in form_wisata:
        biaya_wisata.append(val.biaya)

    
    total_biaya = session["total_biaya"]
    fav, is_fav_exist = show_fav()
    return render_template(
        "pay.html", 
        total=total_biaya, 
        favs=fav, 
        favs_exist=is_fav_exist, 
        formatrupiah=formatrupiah, 
        host=host(),
    )


@home.route("/pay/confirmed", methods=["GET"])
@login_required
def pay_confirmed():
    try:
        id_wisata = session["save_id_wisata"]
    except:
        id_wisata = session["save_id_wisata"] = None
    history = models.Historybelanja(
        id_homestay = session["save_id_homestay"]   ,
        id_user = current_user.get_id(),
        id_wisata = session["save_id_wisata"],
        malam = session["malam"],
        kamar = session["kamar"],
        tgl_check_in = session["ci"],
        tgl_check_out = session["co"]

    )
    models.db.session.add(history)
    models.db.session.commit()

    delete_sessions()
    
    trans = models.Transaksi.query.all()
    for data in trans:
        models.db.session.delete(data)
        models.db.session.commit()
    print("done")
    fav, is_fav_exist = show_fav()

    

    return render_template("pay_confirmed.html", favs=fav, favs_exist=is_fav_exist, host=host())





# @home.route("/homestay/add", methods=["GET", "POST", "PUT", "DELETE"])
# @login_required
# def add_homestay():
#     form = forms.HomestayForm()
#     fav, is_fav_exist = show_fav()
#     if form.validate_on_submit() and request.method == "POST":
#         file = request.files["foto_homestay"]
#         folder = IMAGES_DIR + "/homestay"
#         foto = upload_file(file, folder)  # return random name
#         foto = host() + "/" + foto

#         nama_homestay = validasi_type(form.nama_homestay.data, str)
#         alamat = validasi_type(form.alamat.data, str)
#         deskripsi = validasi_type(form.deskripsi.data, str)
#         fasilitas = validasi_type(form.fasilitas.data, str)
#         jumlah_kamar = validasi_type(form.jumlah_kamar.data, int)
#         harga = validasi_type(form.harga.data, int)
#         diskon = validasi_type(form.diskon.data, int)

#         model = models.Homestay(
#             code_homestay=code_homestay(stringLength=5, gen_for="H"),
#             nama_homestay=nama_homestay,
#             alamat=alamat,
#             deskripsi=deskripsi,
#             fasilitas=fasilitas,
#             harga=harga,
#             diskon=diskon,
#             foto_homestay=foto,
#             jumlah_kamar=jumlah_kamar,
#         )
#         models.db.session.add(model)
#         models.db.session.commit()
#         flash("Homestay berhasil ditambah", "success")
#         return redirect(url_for("home.add_homestay"))
#     return render_template(
#         "add_homestay.html", 
#         form=form, 
#         favs=fav, 
#         favs_exist=is_fav_exist, 
#         host=host(),
#     )


# @home.route("/homestay/wisata/add", methods=["GET", "POST", "PUT", "DELETE"])
# @login_required
# def add_wisata():
#     form = forms.WisataForm()
#     fav, is_fav_exist = show_fav()
#     model_homestay = models.Homestay.query.all()
#     if request.method == "POST":
#         file = request.files["foto_wisata"]
#         # print(file)
#         # return "test"
#         folder = IMAGES_DIR + "/wisata"
#         foto = upload_file(file, folder)  # return random name
#         ip = host()
#         foto = ip + "/" + foto

#         wisata = validasi_type(form.wisata.data, str)
#         fasilitas = validasi_type(form.fasilitas.data, str)
#         biaya = validasi_type(form.biaya.data, str)
#         kegiatan = validasi_type(form.kegiatan.data, str)
#         id_homestay = validasi_type(request.form['id_homestay'], int)

#         model = models.Wisata(
#             code_wisata=code_homestay(stringLength=5, gen_for="W"),
#             wisata=wisata,
#             fasilitas=fasilitas,
#             biaya=biaya,
#             kegiatan=kegiatan,
#             id_homestay=id_homestay,
#             foto_wisata=foto,
#         )
#         models.db.session.add(model)
#         models.db.session.commit()
#         flash("Wisata berhasil ditambah", "success")
#         return redirect(url_for("home.add_wisata"))
#     return render_template(
#         "add_wisata.html", 
#         form=form, favs=fav, 
#         favs_exist=is_fav_exist, 
#         model_homestay=model_homestay,
#     )


@home.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

