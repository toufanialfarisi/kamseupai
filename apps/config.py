import os
from requests import get

DEBUG = True

basedir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///" + os.path.join(basedir, "db/apps.db")

SQLALCHEMY_DATABASE_URI = db_file
SQLALCHEMY_TRACK_MODIFICATIONS = False

THREADS_PER_PAGE = 2

SECRET_KEY = "cBWegL8d367vPzTp9Y2pJudLLtaKi5Jtw8//WsRjZrc="
JWT_SECRET_KEY = "jwt-secret-string"

YOUTUBE_KEY = "AIzaSyAWJFHcvdrpaIr9YoSkrY2vTzcUptqs2O0"
api_service_name = "youtube"
api_version = "v3"


APPLICATION_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(APPLICATION_DIR, "static")
IMAGES_DIR = os.path.join(STATIC_DIR, "images")
# MY_IP = 'http://localhost:5000'

try:
    MY_IP = "http://" + get("https://api.ipify.org").text
except:
    MY_IP = "http://localhost:5000"

