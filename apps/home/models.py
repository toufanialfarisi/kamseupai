from apps import db
import datetime
from apps.auth.models import User


class Homestay(db.Model):
    __tablename__ = "homestay"
    id = db.Column(db.Integer, primary_key=True)
    nama_homestay = db.Column(db.String(80))
    alamat = db.Column(db.TEXT)
    deskripsi = db.Column(db.TEXT)
    fasilitas = db.Column(db.String(100))
    harga = db.Column(db.Integer)
    foto_homestay = db.Column(db.String(255))
    paket_wisata = db.relationship("Wisata", backref="paket_wisata")
    transaksi = db.relationship("Transaksi", backref="transaksi_id")
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    update_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())

    def __repr__(self):
        return f"id_homestay ke-{self.id}"


class Transaksi(db.Model):
    __tablename__ = "transaksi"
    id = db.Column(db.Integer, primary_key=True)
    id_homestay = db.Column(db.Integer, db.ForeignKey("homestay.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"))
    id_wisata = db.Column(db.Integer, db.ForeignKey("wisata.id"))

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False


class Wisata(db.Model):
    __tablename__ = "wisata"
    id = db.Column(db.Integer, primary_key=True)
    wisata = db.Column(db.String(80))
    fasilitas = db.Column(db.String(100))
    biaya = db.Column(db.Integer)
    kegiatan = db.Column(db.TEXT)
    id_homestay = db.Column(db.Integer, db.ForeignKey("homestay.id"))
    transaksi = db.relationship("Transaksi", backref="transaksi_wisata", uselist=False)
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    update_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
