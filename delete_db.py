from apps.home import models
from apps import db

trans = models.Transaksi.query.all()
home = models.Wisa
for data in trans:
    db.session.delete(data)
    db.session.commit()

print("done")

