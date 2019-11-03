from flask_login import (
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required,
    LoginManager,
)
from flask import redirect, url_for, flash, render_template, request, Blueprint, session
from apps.auth_admin.forms import *
from apps.auth_admin.models import *
from apps.auth.models import *
from apps import db
from apps.home.utility import *
from apps.config import IMAGES_DIR, MY_IP
from apps.utils import validasi_type, upload_file
from apps.home.models import Homestay, Wisata, Historybelanja, BuktiBayar, Favorit
from apps.api import provinsi, kabupaten, kecamatan 
from sqlalchemy import desc

import requests
import numpy as np 



admin = Blueprint("admin", __name__, template_folder="templates/")
    
@admin.route("/admin/index", methods=["POST", "GET", "PUT", "DELETE"])
def admin_index():
    if "admin" in session:
        return render_template("index_admin.html", admin=session["admin"], host=host(), n_pesanan=n_pesanan())
    else:
        flash("Silahkan login terlebih dahulu", "danger")
        return redirect(url_for("admin.login_admin"))


@admin.route("/admin/homestay", methods=["POST", "GET", "PUT", "DELETE"])
def view_homestay():
    if "admin" in session:
        page_param = request.args.get("page")
        per_page = 4    
        if not page_param:
            page_param = 1
        paginate = Homestay.query.paginate(page=int(page_param), per_page=per_page)
        max_page = str(paginate.pages)
        curr_page = page_param
        
        next_page = int(page_param) + 1
        next_page = str(next_page)

        prev_page = int(page_param) - 1
        prev_page = str(prev_page)
        form = searchForm()
        if form.validate_on_submit():
            post = Homestay.query.filter(
                Homestay.nama_homestay.like('%' + form.keyword.data + '%')
                ).order_by(Homestay.nama_homestay).paginate(
                page=int(page_param), per_page=per_page
                )
            return render_template(
                'homestay/view_homestay.html', 
                forms=post.items, 
                form=form, 
                no=range(1, len(post.items) + 1),
                host=host(),
                next_page=next_page,
                prev_page=prev_page,
                curr_page=page_param,
                max_page=max_page,
                paginate=paginate,
                n_pesanan=n_pesanan()(),
                
            )
        else:
            return render_template(
            "homestay/view_homestay.html",
            forms=paginate.items,
            form=form,
            no=range(1, len(paginate.items) + 1),
            host=host(),
            next_page=next_page,
            prev_page=prev_page,
            curr_page=page_param,
            max_page=max_page,
            paginate=paginate,
            n_pesanan=n_pesanan(), 
        )
    else:
        flash("Silahkan login terlebih dahulu", "danger")
        return redirect(url_for("admin.login_admin"))


@admin.route("/admin/wisata", methods=["POST", "GET", "PUT", "DELETE"])
def view_wisata():
    if "admin" in session:
        page_param = request.args.get("page")
        per_page = 4    
        if not page_param:
            page_param = 1
        paginate = Wisata.query.paginate(page=int(page_param), per_page=per_page)
        max_page = str(paginate.pages)
        curr_page = page_param
        
        next_page = int(page_param) + 1
        next_page = str(next_page)
        
        prev_page = int(page_param) - 1
        prev_page = str(prev_page)
        form = searchForm()
        if form.validate_on_submit():
            post = Wisata.query.filter(
                Wisata.wisata.like('%' + form.keyword.data + '%')
                ).order_by(Wisata.wisata).paginate(
                page=int(page_param), per_page=per_page
                )
            return render_template(
                'homestay/view_wisata.html', 
                forms=post.items, 
                form=form, 
                no=range(1, len(post.items) + 1),
                host=host(),
                next_page=next_page,
                prev_page=prev_page,
                curr_page=page_param,
                max_page=max_page,
                paginate=paginate,
                n_pesanan=n_pesanan(), 
            )
        else:
            return render_template(
            "homestay/view_wisata.html",
            forms=paginate.items,
            form=form,
            no=range(1, len(paginate.items) + 1),
            host=host(),
            next_page=next_page,
            prev_page=prev_page,
            curr_page=page_param,
            max_page=max_page,
            paginate=paginate,
            n_pesanan=n_pesanan(),
        )
    else:
        flash("Silahkan login terlebih dahulu", "danger")
        return redirect(url_for("admin.login_admin"))


@admin.route("/admin/register", methods=["POST", "GET", "PUT" "DELETE"])
def register_admin():
    form = RegisterForm()
    if form.validate_on_submit():
        admin = Admin(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
        db.session.add(admin)
        db.session.commit()
        flash("Thanks for registration", "success")
        return redirect(url_for("admin.login_admin"))
    return render_template("register_admin.html", form=form)


@admin.route("/admin/login", methods=["POST", "GET"])
def login_admin():

    form = LoginForm()

    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        try:
            if admin.check_password(form.password.data) and admin is not None:
                # if check_password_hash(user.password, form.password.data) and user is
                session["admin"] = form.username.data
                next = request.args.get("next")
                if next == None or not next[0] == "/admin":
                    next = url_for("admin.admin_index")
                return redirect(next)
        except:
            flash("wrong password or username", "danger")
            return redirect(url_for("admin.login_admin"))
    return render_template("login_admin.html", form=form)


@admin.route("/admin/logout")
def logout_admin():
    if "admin" in session:
        session.pop("admin", None)
        return redirect(url_for("admin.login_admin"))
    else:
        flash("Silahkan login terlebih dahulu", "danger")
        return redirect(url_for("admin.login_admin"))


@admin.route("/admin/homestay/add", methods=["GET", "POST", "PUT", "DELETE"])
def add_homestay():
    if "admin" in session:
        form = HomestayForm()
        fav, is_fav_exist = show_fav()
       
        nama = []
        id = []
        url = "http://dev.farizdotid.com/api/daerahindonesia/provinsi"
        data = requests.get(url=url)
        for i in range(len(data.json()["semuaprovinsi"])):
            out = data.json()["semuaprovinsi"][i]["nama"]
            out_id = data.json()["semuaprovinsi"][i]["id"]
            nama.append(out)
            id.append(out_id)
        prov = list(zip(id, nama))

        form.provinsi.choices = [(nama, nama) for id, nama in prov]
        if form.validate_on_submit() and request.method == "POST":
            file = request.files["foto_homestay"]
            folder = IMAGES_DIR + "/homestay"
            foto = upload_file(file, folder)  # return random name
            foto = host() + "/" + foto

            nama_homestay = validasi_type(form.nama_homestay.data, str)
            alamat = validasi_type(form.alamat.data, str)
            provinsi = validasi_type(form.provinsi.data, str)
            deskripsi = validasi_type(form.deskripsi.data, str)
            fasilitas = validasi_type(form.fasilitas.data, str)
            jumlah_kamar = validasi_type(form.jumlah_kamar.data, int)
            harga = validasi_type(form.harga.data, int)
            diskon = validasi_type(form.diskon.data, int)

            model = Homestay(
                code_homestay=code_homestay(stringLength=5, gen_for="H"),
                nama_homestay=nama_homestay,
                alamat=alamat,
                provinsi=provinsi,
                deskripsi=deskripsi,
                fasilitas=fasilitas,
                harga=harga,
                diskon=diskon,
                foto_homestay=foto,
                jumlah_kamar=jumlah_kamar,
            )
            models.db.session.add(model)
            models.db.session.commit()

                
            flash("Homestay berhasil ditambah", "success")

            return redirect(url_for("admin.view_homestay"))
        return render_template(
            "homestay/add_homestay.html",
            form=form,
            favs=fav,
            favs_exist=is_fav_exist,
            host=host(),
            n_pesanan=n_pesanan(),
        )
    else:
        flash("Silahkan login terlebih dahulu", "danger")
        return redirect(url_for("admin.login_admin"))


@admin.route("/admin/homestay/edit/<int:id>", methods=["GET", "POST", "PUT", "DELETE"])
def edit_homestay(id):
    if "admin" in session:
        fav, is_fav_exist = show_fav()
        model = Homestay.query.get(id)
        form = HomestayEditForm(obj=model)

        nama = []
        id = []
        url = "http://dev.farizdotid.com/api/daerahindonesia/provinsi"
        data = requests.get(url=url)
        for i in range(len(data.json()["semuaprovinsi"])):
            out = data.json()["semuaprovinsi"][i]["nama"]
            out_id = data.json()["semuaprovinsi"][i]["id"]
            nama.append(out)
            id.append(out_id)
        prov = list(zip(id, nama))

        form.provinsi.choices = [(nama, nama) for id, nama in prov]
        if form.validate_on_submit() and request.method == "POST":
            try:
                file = request.files["foto_homestay"]
                folder = IMAGES_DIR + "/homestay"
                foto = upload_file(file, folder)  # return random name
                foto = host() + "/" + foto
            except:
                foto = model.foto_homestay

            nama_homestay = validasi_type(form.nama_homestay.data, str)
            alamat = validasi_type(form.alamat.data, str)            
            provinsi = validasi_type(form.provinsi.data, str)
            deskripsi = validasi_type(form.deskripsi.data, str)
            fasilitas = validasi_type(form.fasilitas.data, str)
            jumlah_kamar = validasi_type(form.jumlah_kamar.data, int)
            harga = validasi_type(form.harga.data, int)
            diskon = validasi_type(form.diskon.data, int)
            model.code_homestay = code_homestay(stringLength=5, gen_for="H")
            model.nama_homestay = nama_homestay
            model.alamat = alamat
            model.provinsi = provinsi
            model.deskripsi = deskripsi
            model.fasilitas = fasilitas
            model.harga = harga
            model.diskon = diskon
            model.foto_homestay = foto
            model.jumlah_kamar = jumlah_kamar

            # db.session.add(model)
            db.session.commit()
            flash("Homestay berhasil diedit", "success")
            return redirect(url_for("admin.view_homestay"))
        return render_template(
            "homestay/edit_homestay.html",
            form=form,
            favs=fav,
            favs_exist=is_fav_exist,
            host=host(),
            model=model,
            n_pesanan=n_pesanan(),
        )
    else:
        flash("Silahkan login terlebih dahulu", "danger")
        return redirect(url_for("admin.login_admin"))

@admin.route("/admin/homestay/delete/<int:id>")
def delete_homestay(id):
    if "admin" in session:
        data = Homestay.query.get(id)
        db.session.delete(data)
        db.session.commit()
        flash("Data berhasil dihapus", "success")
        return redirect(url_for("admin.view_homestay"))
    else:
        flash("Silahkan login terlebih dahulu", "danger")
        return redirect(url_for("admin.login_admin"))


@admin.route("/admin/wisata/add", methods=["GET", "POST", "PUT", "DELETE"])
def add_wisata():
    if "admin" in session:
        form = WisataForm()
        fav, is_fav_exist = show_fav()
        model_homestay = Homestay.query.all()
        form.id_homestay.choices = [(form.id, form.nama_homestay) for form in model_homestay]
        if request.method == "POST":
            file = request.files["foto_wisata"]
            # print(file)
            # return "test"
            folder = IMAGES_DIR + "/wisata"
            foto = upload_file(file, folder)  # return random name
            ip = host()
            foto = ip + "/" + foto

            wisata = validasi_type(form.wisata.data, str)
            fasilitas = validasi_type(form.fasilitas.data, str)
            biaya = validasi_type(form.biaya.data, str)
            kegiatan = validasi_type(form.kegiatan.data, str)
            id_homestay = validasi_type(form.id_homestay.data, int)

            model = models.Wisata(
                code_wisata=code_homestay(stringLength=5, gen_for="W"),
                wisata=wisata,
                fasilitas=fasilitas,
                biaya=biaya,
                kegiatan=kegiatan,
                id_homestay=id_homestay,
                foto_wisata=foto,
            )
            models.db.session.add(model)
            models.db.session.commit()
            flash("Wisata berhasil ditambah", "success")
            return redirect(url_for("admin.view_wisata"))

        return render_template(
            "homestay/add_wisata.html",
            form=form,
            favs=fav,
            favs_exist=is_fav_exist,
            model_homestay=model_homestay,
            n_pesanan=n_pesanan(),
        )
    else:
        flash("Silahkan login terlebih dahulu", "danger")
        return redirect(url_for("admin.login_admin"))


@admin.route("/admin/wisata/edit/<int:id>", methods=["GET", "POST", "PUT", "DELETE"])
def edit_wisata(id):
    if "admin" in session:
        model = Wisata.query.get(id)
        form = WisataEditForm(formdata=request.form, obj=model)
        model_homestay = Homestay.query.all()
        form.id_homestay.choices = [(form.id, form.nama_homestay) for form in model_homestay]
        fav, is_fav_exist = show_fav()
        model_homestay = Homestay.query.all()
        if request.method == "POST":
            file = request.files["foto_wisata"]
            folder = IMAGES_DIR + "/wisata"
            foto = upload_file(file, folder)  # return random name
            ip = host()
            foto = ip + "/" + foto

            wisata = validasi_type(form.wisata.data, str)
            fasilitas = validasi_type(form.fasilitas.data, str)
            biaya = validasi_type(form.biaya.data, str)
            kegiatan = validasi_type(form.kegiatan.data, str)
            id_homestay = validasi_type(form.id_homestay.data, int)

            model = Wisata.query.get(id)
            model.code_wisata = code_homestay(stringLength=5, gen_for="W")
            model.wisata = wisata
            model.fasilitas = fasilitas
            model.biaya = biaya
            model.kegiatan = kegiatan
            model.id_homestay = id_homestay
            model.foto_wisata = foto

            models.db.session.add(model)
            models.db.session.commit()
            flash("Wisata berhasil diedit", "success")
            return redirect(url_for("admin.view_wisata"))

        return render_template(
            "homestay/add_wisata.html",
            form=form,
            favs=fav,
            favs_exist=is_fav_exist,
            model_homestay=model_homestay,
            n_pesanan=n_pesanan(),
        )
    else:
        flash("Silahkan login terlebih dahulu", "danger")
        return redirect(url_for("admin.login_admin"))


@admin.route("/admin/wisata/delete/<int:id>")
def delete_wisata(id):
    if "admin" in session:
        data = Wisata.query.get(id)
        db.session.delete(data)
        db.session.commit()
        flash("Data berhasil dihapus", "success")
        return redirect(url_for("admin.view_wisata"))
    else:
        flash("Silahkan login terlebih dahulu", "danger")
        return redirect(url_for("admin.login_admin"))

import copy 

def n_pesanan():
    history = Historybelanja.query.all()
    status = Historybelanja.query.filter_by(status_pesanan=True).all()
    n_pesanan = len(history) - len(status)
    length_history = len(history)
    return n_pesanan

@admin.route("/admin/pesanan", methods=["GET", "POST"])
def pesanan():
    form = searchForm()
    history = Historybelanja.query.all()
    home = Homestay()
    no = np.arange(1,len(history)+1)
    status = Historybelanja.query.filter_by(status_pesanan=True).all()
    n_pesanan = len(history) - len(status)

    page_param = request.args.get("page")
    per_page = 10
    if not page_param:
        page_param = 1
    prev_page = int(page_param) - 1
    prev_page = str(prev_page)
    # user = User.query.get(current_user.get_id)
    data_bukti = BuktiBayar.query.all()
    paginate = Historybelanja.query.paginate(page=int(page_param), per_page=per_page)
    # data_bukti = BuktiBayar()
    return render_template("pesanan.html", data_bukti=data_bukti,form=form, no=no, paginate=paginate, prev_page=prev_page, n_pesanan=n_pesanan, home=home)

@admin.route("/admin/konfirmasi/<id>")
def konfirmasi(id):
    pesanan = Historybelanja.query.get_or_404(id)
    pesanan.status_pesanan = True 
    db.session.add(pesanan)
    db.session.commit()
    return redirect(url_for('admin.pesanan'))

@admin.route("/admin/konfirmasi-kepulangan/<idhomestay>")
def konfirmasi_kepulangan(idhomestay):
    model = Homestay.query.get_or_404(idhomestay)
    model.ketersediaanHomestay = True
    db.session.add(model)
    db.session.commit()
    return redirect(url_for('admin.pesanan'))


@admin.route("/admin/slider/add", methods=["POST", "GET"])
def add_slider():
    form = SliderForm()
    if form.validate_on_submit() or request.method == "POST":
        file = request.files["image"]
        folder = IMAGES_DIR + "/slider"
        foto = upload_file(file, folder)  # return random name
        foto = host() + "/" + foto

        model = Slider(image=foto)
        models.db.session.add(model)
        models.db.session.commit()
        flash("Slider berhasil ditambahkan", "success")
        return redirect(url_for("admin.view_slider"))

    return render_template("slider/add_slider.html", form=form)

@admin.route("/admin/slider", methods=["GET"])
def view_slider():
    form = SliderForm()
    page_param = request.args.get("page")
    per_page = 4    
    paginate = Slider.query.paginate(page=page_param, per_page=per_page)
    no=range(1, len(paginate.items) + 1)
    return render_template("slider/view_slider.html", forms=paginate.items, no=no)

@admin.route("/admin/slider/<int:id>", methods=["GET"])
def delete_slider(id):
    data = Slider.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("admin.view_slider"))