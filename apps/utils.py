from werkzeug.utils import secure_filename
import base64
import random
import string
from datetime import datetime
import os


def validasi_type(name, typenya, require=False):
    # if require == True:
    #     return name
    try:
        assert type(name) == typenya
    except:
        if type(name) != typenya:
            name = int(name)
        else:
            name = str(name)
    return name


def custom_response(code=200, data=[], msg=None, meta=None):
    return {"message": msg, "data": data, "meta": meta, "code": code}


def random_string(jumlah):
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(jumlah)
    )


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in set(
        ["txt", "pdf", "png", "jpg", "jpeg", "gif"]
    )


def upload_file(file, folder):
    if file and allowed_file(file.filename):
        nama = file.filename
        if not os.path.exists(folder):
            os.makedirs(folder)
        extensi = "." in nama and nama.rsplit(".", 1)[1].lower()
        nama = (
            "." in nama
            and nama.rsplit(".", 1)[0].upper()[:0]
            + random_string(3)
            + "_"
            + str(datetime.now())[:18]
            + "."
            + extensi
        )
        nama = secure_filename(nama)
        file.save(os.path.join(folder, nama))
        link = str(os.path.join(folder, nama)).split("/")
        return str("/".join(link[-4:]))
    else:
        raise


# with open("imageToSave.png", "wb") as fh:
#     fh.write(base64.decodebytes(foto))#from btoa string javascript
