from datetime import datetime
from apps.config import MY_IP
from apps.home import models
from flask_login import current_user
import random
import string
import os

host_mode = os.getenv("HOST_MODE")


def host(localhost=host_mode):
    if localhost == "localhost":
        host = "http://localhost"
        return host

    elif localhost == "production_to_heroku":
        host = "http://kamseupai.herokuapp.com"
        return host
    else:
        host = MY_IP
        return host


def custom_session_idhomestay(homestay_id):
    id_homestay = models.Homestay.query.get(homestay_id)
    return id_homestay


def show_fav():
    fav = models.Favorit.query.filter_by(id_user=current_user.get_id()).all()
    if fav:
        is_fav_exist = True
    else:
        is_fav_exist = False
    return fav, is_fav_exist


def formatrupiah(uang):
    y = str(uang)
    if len(y) <= 3:
        return y
    else:
        p = y[-3:]
        q = y[:-3]
        return formatrupiah(q) + "." + p


def tanggal_checkout(n_malam, tanggal_checkin, bulan_checkin):
    feb_kabisat = datetime.utcnow().date().day
    jan = 31
    if feb_kabisat == 29:
        feb = 29
    else:
        feb = 28

    mar = 30
    apr = 30
    may = 31
    jun = 30
    jul = 31
    aug = 31
    sep = 30
    okt = 31
    nov = 30
    dec = 31

    end_month = ["", jan, feb, mar, apr, may, jun, jul, aug, sep, okt, nov, dec]

    end_month_str = [
        "",
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "okt",
        "nov",
        "dec",
    ]

    n_malam = n_malam
    tanggal_checkin = tanggal_checkin
    out = tanggal_checkin + n_malam
    bulan_now = end_month[bulan_checkin]
    if out >= bulan_now:
        sis = out - bulan_now
        checkout = sis
        return checkout, end_month_str.index(end_month_str[bulan_checkin + 1])
    else:
        return tanggal_checkin + n_malam


def code_homestay(stringLength=6, gen_for="H"):
    """Generate a random string of letters and digits """
    lettersAndDigits = gen_for + string.ascii_letters + string.digits
    return "".join(random.choice(lettersAndDigits) for i in range(stringLength))
