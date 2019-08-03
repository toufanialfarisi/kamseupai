import requests


def provinsi():
    nama = []
    id = []
    url = "http://dev.farizdotid.com/api/daerahindonesia/provinsi"
    data = requests.get(url=url)
    for i in range(len(data.json()["semuaprovinsi"])):
        out = data.json()["semuaprovinsi"][i]["nama"]
        out_id = data.json()["semuaprovinsi"][i]["id"]
        nama.append(out)
        id.append(out_id)
    return nama, id


def kabupaten(id_provinsi):
    # ex : id_provinsi = 11
    url = f"http://dev.farizdotid.com/api/daerahindonesia/provinsi/{id_provinsi}/kabupaten"
    data = requests.get(url=url)
    nama = []
    id = []
    len_data = data.json()["kabupatens"]
    for i in range(len(len_data)):
        out = data.json()["kabupatens"][i]["nama"]
        out_id = data.json()["kabupatens"][i]["id"]
        nama.append(out)
        id.append(out_id)
    return nama, id


def kecamatan(id_kabupaten):
    # ex : id_kabupaten = 11
    url = f"http://dev.farizdotid.com/api/daerahindonesia/provinsi/kabupaten/{id_kabupaten}/kecamatan"
    data = requests.get(url=url)
    nama = []
    id = []
    len_data = data.json()["kecamatans"]
    for i in range(len(len_data)):
        out = data.json()["kecamatans"][i]["nama"]
        out_id = data.json()["kecamatans"][i]["id"]
        nama.append(out)
        id.append(out_id)
    return nama, id

