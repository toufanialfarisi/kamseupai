from apps import db
import datetime
from apps.auth.models import User


class Homestay(db.Model):
    __tablename__ = "homestay"
    id = db.Column(db.Integer, primary_key=True)
    nama_homestay = db.Column(db.String(80))
    code_homestay = db.Column(db.String(10))
    alamat = db.Column(db.TEXT)
    deskripsi = db.Column(db.TEXT)
    fasilitas = db.Column(db.String(100))
    harga = db.Column(db.Integer)
    diskon = db.Column(db.Integer)
    foto_homestay = db.Column(db.String(255))
    paket_wisata = db.relationship("Wisata", backref="paket_wisata")
    transaksi = db.relationship("Transaksi", backref="transaksi_id")
    favoritkan = db.relationship("Favorit", backref="list_favorit")
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    update_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return f"homestay : -{self.nama_homestay}"


class Transaksi(db.Model):
    __tablename__ = "transaksi"
    id = db.Column(db.Integer, primary_key=True)
    id_homestay = db.Column(db.Integer, db.ForeignKey("homestay.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_wisata = db.Column(db.Integer, db.ForeignKey("wisata.id"))
    malam = db.Column(db.Integer)


class BelanjaUser(db.Model):
    __tablename__ = "belanjauser"
    id = db.Column(db.Integer, primary_key=True)
    homestay_book = db.Column(db.String(50))
    wisata_book = db.Column(db.String(50))
    malam = db.Column(db.Integer)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))


class Wisata(db.Model):
    __tablename__ = "wisata"
    id = db.Column(db.Integer, primary_key=True)
    code_wisata = db.Column(db.String(10))
    wisata = db.Column(db.String(80))
    fasilitas = db.Column(db.String(100))
    biaya = db.Column(db.Integer)
    kegiatan = db.Column(db.TEXT)
    foto_wisata = db.Column(db.String(100))
    diskon = db.Column(db.Integer)
    id_homestay = db.Column(db.Integer, db.ForeignKey("homestay.id"))
    transaksi = db.relationship("Transaksi", backref="transaksi_wisata", uselist=False)
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    update_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())


class HomeSession(db.Model):
    __tablename__ = "id_home_session"
    id = db.Column(db.Integer, primary_key=True)
    id_homestay = db.Column(db.Integer)
    user_now = db.Column(db.Integer, db.ForeignKey("user.id"))


class WisataSession(db.Model):
    __tablename__ = "id_wisata_session"
    id = db.Column(db.Integer, primary_key=True)
    id_wisata = db.Column(db.Integer)
    user_now = db.Column(db.Integer, db.ForeignKey("user.id"))


class Favorit(db.Model):
    __tablename__ = "favorit"
    id = db.Column(db.Integer, primary_key=True)
    fav_homestay = db.Column(db.String(100))
    id_homestay = db.Column(db.Integer, db.ForeignKey("homestay.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
