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
    submit = SubmitField("Tambah Wisata")


class HomestayForm(FlaskForm):
    nama_homestay = StringField("Nama homestay", validators=[DataRequired()])
    alamat = StringField("Alamat", validators=[DataRequired()])
    deskripsi = TextAreaField("Deskripsi", validators=[DataRequired()])
    fasilitas = StringField("Fasilitas", validators=[DataRequired()])
    harga = IntegerField("Harga", validators=[DataRequired()])
    foto_homestay = FileField(validators=[FileRequired()])
    submit = SubmitField("Tambah Homestay")
