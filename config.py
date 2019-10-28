import os

file_path = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.join(file_path, "data.sqlite")
# database
db_config = {
    "production": {
        "db_type": "postgresql",
        "username": "rqjlcbouwdptml",
        "password": "140d296ff6a2103213affa9eaeaa8b3f2d24cb15c1b9a321ce77277db35bca55",
        "host": "ec2-54-197-238-238.compute-1.amazonaws.com",
        "port": "5432",
        "database": "da3kp68t3m2lui",
    },
    "development": {
        "db_type": "mysql",
        "username": "kamseupai",
        "password": "kampungantapisukses",
        "host": "localhost",
        "port": "5432",
        "database": "monolitik",
    },
}


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
        db_config["production"]["db_type"],
        db_config["production"]["username"],
        db_config["production"]["password"],
        db_config["production"]["host"],
        db_config["production"]["port"],
        db_config["production"]["database"],
    )


class StaggingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
        db_config["development"]["db_type"],
        db_config["development"]["username"],
        db_config["development"]["password"],
        db_config["development"]["host"],
        db_config["development"]["port"],
        db_config["development"]["database"],
    )


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
        db_config["development"]["db_type"],
        db_config["development"]["username"],
        db_config["development"]["password"],
        db_config["development"]["host"],
        db_config["development"]["port"],
        db_config["development"]["database"],
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + basedir
