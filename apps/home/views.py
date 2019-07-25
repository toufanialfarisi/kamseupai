from flask import redirect, url_for, flash, render_template, request, Blueprint
from apps.home import forms, models
from apps.utils import validasi_type, upload_file
from apps.config import IMAGES_DIR, MY_IP

home = Blueprint("home", __name__, template_folder="templates/")


@home.route("/", methods=["GET"])
def index():
    return render_template("home.html")


@home.route("/homestay/add", methods=["GET", "POST", "PUT", "DELETE"])
def add_homestay():
    form = forms.HomestayForm()

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
    return render_template("add_homestay.html", form=form)


@home.route("/homestay/wisata/add", methods=["GET", "POST", "PUT", "DELETE"])
def add_wisata():
    form = forms.WisataForm()
    if request.method == "POST" and form.validate_on_submit():

        wisata = validasi_type(form.wisata.data, str)
        fasilitas = validasi_type(form.fasilitas.data, str)
        biaya = validasi_type(form.biaya.data, str)
        kegiatan = validasi_type(form.biaya.data, int)
        id_homestay = validasi_type(form.id_homestay.data, int)

        model = models.Wisata(
            wisata=wisata,
            fasilitas=fasilitas,
            biaya=biaya,
            kegiatan=kegiatan,
            id_homestay=id_homestay,
        )
        models.db.session.add(model)
        models.db.session.commit()
        flash("Wisata berhasil ditambah", "success")
        return redirect(url_for("home.add_wisata"))
    return render_template("add_wisata.html", form=form)

