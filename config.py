import os


basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo')
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = False

WTF_CSRF_ENABLED = True

RECAPTCHA_PUBLIC_KEY = "6Lf7URkUAAAAAPSLqnmvSEjQ17RX573UvgLGE4J_"
RECAPTCHA_PRIVATE_KEY = "6Lf7URkUAAAAALcZ9mWGeidHWpe-Kv8Z_Aku202G"
RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}