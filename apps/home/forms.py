from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (
    StringField,
    StringField,
    TextAreaField,
    SubmitField,
    IntegerField,
    SelectField,
)
from wtforms.validators import DataRequired
from apps.home import models


def choice_query():
    return models.Homestay.query


class WisataForm(FlaskForm):
    wisata = StringField("Wisata", validators=[DataRequired()])
    fasilitas = StringField("Fasilitas", validators=[DataRequired()])
    kegiatan = TextAreaField("Kegiatan", validators=[DataRequired()])
    biaya = IntegerField("Biaya", validators=[DataRequired()])
    id_homestay = SelectField(
        "Select Id Homestay",
        choices=[(k.id, k.nama_homestay) for k in models.Homestay.query.all()],
        coerce=int,
    )
    foto_wisata = FileField(validators=[FileRequired()])
    submit = SubmitField("Tambah Wisata")


class HomestayForm(FlaskForm):
    nama_homestay = StringField("Nama homestay", validators=[DataRequired()])
    alamat = StringField("Alamat", validators=[DataRequired()])
    deskripsi = TextAreaField("Deskripsi", validators=[DataRequired()])
    fasilitas = StringField("Fasilitas", validators=[DataRequired()])
    jumlah_kamar = IntegerField("Jumlah kamar", validators=[DataRequired()])
    harga = IntegerField("Harga", validators=[DataRequired()])
    diskon = IntegerField("Diskon", validators=[DataRequired()])
    foto_homestay = FileField(validators=[FileRequired()])
    submit = SubmitField("Tambah Homestay")


class searchForm(FlaskForm):
    keyword = StringField("Keyword", render_kw={"placeholder": "Kata kunci"})
    submit = SubmitField("Cari")


class UserDetailForm(FlaskForm):
    nama_lengkap = StringField("Nama Lengkap")
    jenis_kelamin = SelectField("Jenis Kelamin", choices=[])
    nomor_hp = StringField("Nomor HP")
    alamat = TextAreaField("Alamat Lengkap")
    foto_user = FileField("Foto Profil")
    submit = SubmitField("Update Profile")


class BuktiBayarForm(FlaskForm):
    nama_rek = StringField("Nama Pemilik Rekening", validators=[DataRequired()])
    bank_tujuan = SelectField(
        "Bank Tujuan Transfer",
        choices=[("", ""), ("mandiri", "mandiri"), ("BNI", "BNI")],
        validators=[FileRequired()],
    )
    foto_bukti = FileField("Foto Bukti Pembayaran")
    submit = SubmitField("Konfirmasi")
