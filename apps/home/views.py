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
from apps.auth.models import UserDetail, User
from flask_login import login_user

home = Blueprint("home", __name__, template_folder="templates/")

def current_username():
    try:
        query = models.User.query.get(current_user.get_id())
        username = query.username
        return username
    except:
        return redirect(url_for('auth.login'))

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

def foto_profile_user():
    try:
        user_pro = UserDetail.query.get(current_user.get_id())
        img_user = user_pro.foto_user
        return img_user
    except:
        img_user = None 
        return img_user



@home.route("/", methods=["GET", "POST"])
def index():
    ls_curency = []
    model = models.Homestay.query.all()
    page_param = request.args.get("page")
    per_page = 5    
    if not page_param:
        page_param = 1
    paginate = Homestay.query.paginate(page=int(page_param), per_page=per_page)
    max_page = str(paginate.pages)
    curr_page = page_param
    
    next_page = int(page_param) + 1
    next_page = str(next_page)

    prev_page = int(page_param) - 1
    prev_page = str(prev_page)

    fav, is_fav_exist = show_fav()
    ls_diskon = []
    for cur in paginate.items:
        rupiah = formatrupiah(cur.harga)
        ls_curency.append(rupiah)
        real_harga = cur.harga 
        potongan_harga = cur.harga * (cur.diskon/100)
        disk = int(real_harga - potongan_harga)
        thediskon = formatrupiah(disk)
        ls_diskon.append(thediskon)
    
    searchform = searchForm()
    if searchform.validate_on_submit():
        post = Homestay.query.filter(
                Homestay.nama_homestay.like('%' + searchform.keyword.data + '%')
                ).order_by(Homestay.nama_homestay).paginate(
                page=int(page_param), per_page=per_page
                )
        
        return render_template(
            "home.html", 
            formm=searchform,
            form=post.items, 
            favs=fav, 
            favs_exist=is_fav_exist, 
            rupiah=ls_curency, 
            ls_diskon=ls_diskon,
            host=host(),
            next_page=next_page,
            prev_page=prev_page,
            curr_page=page_param,
            max_page=max_page,
            paginate=paginate,
            img_user=foto_profile_user(),
            username = current_username(),
        )
    
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        try:
            check_user_confirmed = user.confirmation_status
            if (
                user.check_password(request.form["password"])
                and user is not None
                and check_user_confirmed is True
            ):

                login_user(user)
                next = request.args.get("next")
                if next == None or not next[0] == "/":
                    next = url_for("home.index")
                return redirect(next)
            elif (
                user.check_password(request.form["password"])
                and user is not None
                and check_user_confirmed is False
            ):
                flash("Akun belum terkonfirmasi, silahkan cek email Anda !", "danger")
                return redirect(url_for("auth.login"))
            else:
                flash("Username / password Anda salah", "danger")
                return redirect(url_for("auth.login"))

        except AttributeError:
            flash("Akun anda tidak terdaftar, silahkan register dulu !", "danger")
            return redirect(url_for("auth.login"))
    
    try:
        user_model = UserDetail.query.filter_by(id_user=current_user.get_id()).first()
        if current_user.is_authenticated:
            if user_model.nama_lengkap is None:
                flash("Silahkan lengkapi / perbaharui informasi profil Anda", "info")
            else:
                pass 
        else:
            pass 
    except:
        pass 

    try:
        user_favorit = models.Favorit.query.filter_by(id_user=current_user.get_id()).first()
        status_favor = user_favorit.query.filter_by(status=True).first()
        favor=status_favor.status
    except:
        favor=False
        
    return render_template(
        "home.html", 
        formm=searchform,
        form=paginate.items, 
        favs=fav, 
        favs_exist=is_fav_exist, 
        rupiah=ls_curency, 
        ls_diskon=ls_diskon,
        next_page=next_page,
        prev_page=prev_page,
        curr_page=page_param,
        max_page=max_page,
        paginate=paginate,
        img_user=foto_profile_user(),
        username = current_username(),
        fav=favor,
        homestay=models.Homestay(),
        
        )


@home.route("/favorit/<int:id>", methods=["GET"])
@login_required
def favorit(id):
    query_fav = models.Favorit.query.filter_by(id_user=current_user.get_id()).all()
    try:
        for dt in query_fav:
            # lanjutkan program jika id_homestay nggak sama dengan id
            # kalau sama, maka error kan 
            assert dt.id_homestay != id 
    except:
        return redirect(url_for("home.index"))
    user_now = current_user.get_id()
    model_homestay = models.Homestay.query.get(id)
    fav = models.Favorit(fav_homestay=model_homestay.nama_homestay, id_homestay=model_homestay.id, id_user=user_now, status=True)
    models.db.session.add(fav)
    models.db.session.commit()
    flash("{} berhasil ditambahkan ke favorit".format(model_homestay.nama_homestay), "success")
    return redirect(url_for("home.index"))

@home.route("/remove/favorit/<int:id>", methods=["GET"])
@login_required
def remove_favorit(id):
    data = models.Favorit.query.get(id)
    models.db.session.delete(data)
    models.db.session.commit()
    return redirect(url_for("home.index"))


@home.route("/checkout/favorit/<int:id>", methods=["GET"])
@login_required
def checkout_favorit(id):
    user_now = current_user.get_id()
    model_homestay = models.Homestay.query.get(id)
    fav = models.Favorit(fav_homestay=model_homestay.nama_homestay,id_homestay=model_homestay.id, id_user=user_now)
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
    searchform = searchForm()
    if request.method == "POST":

        if request.form["malam"] and request.form["kamar"] and request.form["malam"] and request.form["check_in"] and request.form["nama_lengkap"] and request.form["no_ktp"] or request.form["no_passport"]:
            session["no_ktp"] = request.form["no_ktp"]
            session["save_id_homestay"] = id
            session["nama_lengkap"] = request.form["nama_lengkap"]
            if request.form["no_passport"]:
                session["no_passport"] = request.form["no_passport"]
            else:
                session["no_passport"] = None 
            
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
            
            if model_wisata:
                return redirect(url_for("home.book_homestay", id=id))
            else:    
                return redirect(url_for("home.checkout"))
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
        formm=searchform,
        img_user=foto_profile_user(),
        username = current_username(),
        homestay=models.Homestay(),
    )


@home.route("/book/homestay/<int:id>", methods=["GET", "POST"])
@login_required
def book_homestay(id):
    model = models.Homestay.query.get(id)
    session["save_id_homestay"] = id
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
        img_user=foto_profile_user(),
        username = current_username(),
        homestay=models.Homestay(),
    )


@home.route("/book/homestay/wisata/<int:id>", methods=["GET"])
@login_required
def book_wisata(id):
    session["save_id_wisata"] = id   
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
        img_user=foto_profile_user(),
        username = current_username(),
        homestay=models.Homestay(),
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
        img_user=foto_profile_user(),
        username = current_username(),
        homestay=models.Homestay(),
    )


@home.route("/pay/confirmed", methods=["GET"])
@login_required
def pay_confirmed():
    # if "save_id_wisata" in session and "save_id_wisata" in session and "nama_lengkap" in session and "no_ktp" in session and "malam" in session and "kamar" in session and "ci" in session and "co" in session:
    if "malam" in session:
        try:
            id_wisata = session["save_id_wisata"]
        except:
            id_wisata = session["save_id_wisata"] = None
        history = models.Historybelanja(
            id_homestay = session["save_id_homestay"]   ,
            id_user = current_user.get_id(),
            id_wisata = session["save_id_wisata"],
            nama_lengkap = session["nama_lengkap"],
            no_ktp = session["no_ktp"],
            no_passport = session["no_passport"],
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
        
        fav, is_fav_exist = show_fav()

        return render_template(
            "pay_confirmed.html", 
            favs=fav, 
            favs_exist=is_fav_exist, 
            host=host(), 
            img_user=foto_profile_user(), 
            username = current_username(),
            homestay=models.Homestay(),
        )
    else:
        progress = url_for("home.index")
        return render_template("kembali.html", progress=progress)
    


@home.route("/user-detail", methods=["POST", "GET"])
@login_required
def user_detail():
    fav, is_fav_exist = show_fav()
    user_id = current_user.get_id()
    user_form = UserDetailForm()
    query_user = User.query.get(user_id) 
    user_detail = UserDetail.query.filter_by(id_user=user_id).first()
    return render_template(
        "user_detail.html", 
        form=user_detail, 
        form_user=query_user, 
        img_user=foto_profile_user(),
        formm=searchForm(),
        username = current_username(),
        favs=fav,
        homestay=models.Homestay(),
        
    )

    
@home.route("/edit-user", methods=["GET", "POST"])
@login_required
def edit_user():
    fav, is_fav_exist = show_fav()
    user_id = current_user.get_id()
    user_detail = UserDetail.query.get(user_id)
    form = UserDetailForm(obj=user_detail)
    form.jenis_kelamin.choices = [("Pria", "Pria"), ("Wanita", "Wanita")]
    if form.validate_on_submit():
        try:
            file = request.files["foto_user"]
            folder = IMAGES_DIR + "/wisata"
            foto = upload_file(file, folder)  # return random name
            ip = host()
            foto = ip + "/" + foto
        except:
            foto = user_detail.foto_user

        model = UserDetail.query.get(user_id)
        model.nama_lengkap = form.nama_lengkap.data
        model.jenis_kelamin = form.jenis_kelamin.data
        model.nomor_hp = form.nomor_hp.data
        model.alamat = form.alamat.data
        model.foto_user = foto
        models.db.session.add(model)
        models.db.session.commit()
        
        return redirect(url_for('home.user_detail'))


    return render_template(
        "user_detail_edit.html", 
        form=form, 
        img_user=foto_profile_user(), 
        formm=searchForm(),
        username = current_username(),
        favs=fav,
        homestay=models.Homestay(),
    )



@home.route("/status-pesanan")
@login_required
def status_pesanan():
    '''
    filter semua historybelanja berdasarkan id_usernya
    id_homestay dan belanja ini saya looping 

    '''
    id_homestay = []
    belanja = Historybelanja.query.filter_by(id_user=current_user.get_id()).all()

    for i in belanja:
        id_homestay.append(i.id_homestay)
    
    home = Homestay()
    return render_template(
        "status_pesanan.html", 
        id_homestay=id_homestay, # satu
        form_belanja=belanja, # banyak
        home=home,
        img_user=foto_profile_user(),
        username = current_username(),
        formm=searchForm(),
        homestay=models.Homestay(),
    )

@home.route("/proses-pembayaran")
@login_required
def proses_pembayaran():
    # return redirect(url_for('home.pay_confirmed'))
    progress = url_for('home.pay_confirmed')
    return render_template(
        "proses_pembayaran.html", 
        progress=progress, 
        img_user=foto_profile_user(), 
        homestay=models.Homestay(),
    )

@home.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

