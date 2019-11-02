import os

# CONFIG FILE
file_path = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.join(file_path, "data.sqlite")


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
    OAUTHLIB_RELAX_TOKEN_SCOPE = os.getenv("OAUTHLIB_RELAX_TOKEN_SCOPE")
    OAUTHLIB_INSECURE_TRANSPORT = os.getenv("OAUTHLIB_INSECURE_TRANSPORT")


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
        os.environ["db_type"],
        os.environ["username"],
        os.environ["password"],
        os.environ["host"],
        os.environ["port"],
        os.environ["database"],
    )
    # SERVER_NAME = "kamseupai.herokuapp.com"


class StaggingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
        os.environ["db_type"],
        os.environ["username"],
        os.environ["password"],
        os.environ["host"],
        os.environ["port"],
        os.environ["database"],
    )


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
        os.environ["db_type"],
        os.environ["username"],
        os.environ["password"],
        os.environ["host"],
        os.environ["port"],
        os.environ["database"],
    )
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestingConfig(Config):
    TESTING = True
    DEVBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + basedir
