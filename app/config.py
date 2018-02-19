import os


class Configuration(object):
    DEBUG = True
    SECRET_KEY = 'super secret key right here. Seriously, it is SECRET!'
    BCRYPT_LOG_ROUNDS = 15

    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/rr.db' % APPLICATION_DIR

    SQLALCHEMY_TRACK_MODIFICATIONS = False
