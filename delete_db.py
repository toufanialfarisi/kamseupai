from apps.auth import models
from apps import db

trans = models.User.query.all()
for data in trans:
    db.session.delete(data)
    db.session.commit()

print("done")

# db.reflect()
# db.drop_all()
# print("DB CLEAR")
