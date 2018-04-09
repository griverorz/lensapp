from __future__ import absolute_import
import sys

sys.path.append("..")

from celeryconfig import (broker_url,
                          result_backend,
                          mongodb_backend_settings)


class Config(object):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    CELERY_BROKER_URL = broker_url
    CELERY_RESULT_BACKEND = result_backend
    UPLOAD_FOLDER = "."
    MONGO_URI = mongodb_backend_settings


class ProdConfig(Config):
    DEBUG = False
    CELERY_BROKER_URL = broker_url
    CELERY_RESULT_BACKEND = result_backend
    UPLOAD_FOLDER = "."
    MONGO_URI = mongodb_backend_settings
