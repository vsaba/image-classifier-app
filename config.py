import os


class Default(object):
    """
    Base configurations for application
    """
    SECRET_KEY = 'My secret key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
    PATH_TO_IMAGES = 'flaskr/static/images'
    TOKEN_SERIALIZER_SALT = 'token_salt'

    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'ac8aa3a417d060'
    MAIL_PASSWORD = '7b492d3ee09491'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    DEFAULT_APPLICATION_SENDER_EMAIL = 'interviewapplication98@gmail.com'
    PATH_TO_CLASSIFIER_MODEL = "classifier/mnist_model.pt"


class Testing(Default):
    """Testing configuration for the application"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


class Production(Default):
    """
    Production configuration for the application.
    To be used exclusively in a docker image
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://gattito:gattito1234@db:5432/classifier_app_db'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'interviewapplication98@gmail.com'
    MAIL_PASSWORD = os.getenv('GMAIL_PASSKEY')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
