from apps import db
import datetime
from apps.auth.models import User


class Homestay(db.Model):
    __tablename__ = "homestay"
    id = db.Column(db.Integer, primary_key=True)
    nama_homestay = db.Column(db.String(80))
    code_homestay = db.Column(db.String(10))
    alamat = db.Column(db.TEXT)
    provinsi = db.Column(db.String(100))
    deskripsi = db.Column(db.TEXT)
    fasilitas = db.Column(db.String(100))
    harga = db.Column(db.Integer)
    diskon = db.Column(db.Integer)
    foto_homestay = db.Column(db.String(255))
    jumlah_kamar = db.Column(db.Integer)
    paket_wisata = db.relationship("Wisata", backref="paket_wisata")
    transaksi = db.relationship("Transaksi", backref="transaksi_id")
    history_belanja = db.relationship("Historybelanja", backref="history_belanja_user")
    favoritkan = db.relationship("Favorit", backref="list_favorit")
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    update_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    ketersediaanHomestay = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"homestay : -{self.nama_homestay}"


class Transaksi(db.Model):
    __tablename__ = "transaksi"
    id = db.Column(db.Integer, primary_key=True)
    id_homestay = db.Column(db.Integer, db.ForeignKey("homestay.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_wisata = db.Column(db.Integer, db.ForeignKey("wisata.id"))
    malam = db.Column(db.Integer)
    kamar = db.Column(db.Integer)
    tgl_check_in = db.Column(db.String(10))
    tgl_check_out = db.Column(db.String(10))


class Historybelanja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_homestay = db.Column(db.Integer, db.ForeignKey("homestay.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_wisata = db.Column(db.Integer, db.ForeignKey("wisata.id"))
    nama_lengkap = db.Column(db.String(100))
    no_ktp = db.Column(db.String(100))
    no_passport = db.Column(db.String(100))
    malam = db.Column(db.Integer)
    kamar = db.Column(db.Integer)
    tgl_check_in = db.Column(db.DATE)
    tgl_check_out = db.Column(db.DATE)
    status_pesanan = db.Column(
        db.Boolean, default=False
    )  # False (0) = sudah dibooking, True (1) = tersedia/belum dibooking
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    bukti_resi = db.relationship("BuktiBayar", backref="bukti_pembayaran")


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
    history_belanja = db.relationship(
        "Historybelanja", backref="history_belanja_wisata", uselist=False
    )
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
    status = db.Column(db.Boolean, default=False)


class BuktiBayar(db.Model):
    __tablename__ = "bukti_bayar"
    id = db.Column(db.Integer, primary_key=True)
    id_history_belanja = db.Column(db.Integer, db.ForeignKey("historybelanja.id"))
    nama_rek = db.Column(db.String(100))
    bank_tujuan = db.Column(db.String(100))
    foto_bukti = db.Column(db.String(100))
