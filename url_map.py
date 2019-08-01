from app import app

url_map = str(app.url_map)
with open("url_map.txt", "w+") as w:
    w.write(url_map)

