from apps.home import models
from apps import db

trans = models.User.query.all()
for data in trans:
    db.session.delete(data)
    db.session.commit()

print("done")

