from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    BooleanField,
    IntegerField,
    SelectField,
)
from apps.auth_admin.models import Admin
from flask_wtf.file import FileField, FileRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("remember")
    submit = SubmitField("Log in")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_email(self, field):

        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered !")

    def validate_username(self, field):

        if Admin.query.filter_by(username=field.data).first():
            raise ValidationError("Sorry, that username is registered !")


class HomestayForm(FlaskForm):
    nama_homestay = StringField("Nama homestay", validators=[DataRequired()])
    alamat = StringField("Alamat", validators=[DataRequired()])
    provinsi = SelectField("Provinsi", choices=[], validators=[DataRequired()])
    deskripsi = TextAreaField("Deskripsi", validators=[DataRequired()])
    fasilitas = StringField("Fasilitas", validators=[DataRequired()])
    jumlah_kamar = IntegerField("Jumlah kamar", validators=[DataRequired()])
    harga = IntegerField("Harga", validators=[DataRequired()])
    diskon = IntegerField("Diskon", validators=[DataRequired()])
    foto_homestay = FileField(validators=[FileRequired()])
    submit = SubmitField("Tambah Homestay")


class HomestayEditForm(FlaskForm):
    nama_homestay = StringField("Nama homestay", validators=[DataRequired()])
    alamat = StringField("Alamat", validators=[DataRequired()])
    provinsi = SelectField("Provinsi", choices=[], validators=[DataRequired()])
    deskripsi = TextAreaField("Deskripsi", validators=[DataRequired()])
    fasilitas = StringField("Fasilitas", validators=[DataRequired()])
    jumlah_kamar = IntegerField("Jumlah kamar", validators=[DataRequired()])
    harga = IntegerField("Harga", validators=[DataRequired()])
    diskon = IntegerField("Diskon")
    foto_homestay = FileField("Foto Homestay")
    submit = SubmitField("Edit Homestay")


class WisataForm(FlaskForm):
    wisata = StringField("Wisata", validators=[DataRequired()])
    fasilitas = StringField("Fasilitas", validators=[DataRequired()])
    kegiatan = TextAreaField("Kegiatan", validators=[DataRequired()])
    biaya = IntegerField("Biaya", validators=[DataRequired()])
    foto_wisata = FileField(validators=[FileRequired()])
    id_homestay = SelectField("Homestay", choices=[], validators=[DataRequired()])
    submit = SubmitField("Tambah Wisata")


class WisataEditForm(FlaskForm):
    wisata = StringField("Wisata", validators=[DataRequired()])
    fasilitas = StringField("Fasilitas", validators=[DataRequired()])
    kegiatan = TextAreaField("Kegiatan", validators=[DataRequired()])
    biaya = IntegerField("Biaya", validators=[DataRequired()])
    foto_wisata = FileField(validators=[FileRequired()])
    id_homestay = SelectField("Homestay", choices=[], validators=[DataRequired()])
    submit = SubmitField("Edit Atraksi")


class searchForm(FlaskForm):
    keyword = StringField("Keyword", render_kw={"placeholder": "Kata kunci"})
    submit = SubmitField("Cari")


class SliderForm(FlaskForm):
    image = FileField("Tambah Image slider", validators=[FileRequired()])
    submit = SubmitField("Tambah")
