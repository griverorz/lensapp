from __future__ import absolute_import

broker_url = 'amqp://guest:guest@rabbitmq:5672//'
result_backend = 'redis://redis:6379/0'


class Config(object):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    CELERY_BROKER_URL = broker_url
    CELERY_RESULT_BACKEND = result_backend
    UPLOAD_FOLDER = "."


class ProdConfig(Config):
    DEBUG = False
    CELERY_BROKER_URL = broker_url
    CELERY_RESULT_BACKEND = result_backend
    UPLOAD_FOLDER = "."
