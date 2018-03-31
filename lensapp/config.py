from __future__ import absolute_import

broker_url = 'redis://redis:6379/0'
result_backend = 'redis://redis:6379/0'

imports = ("lensapp.tasks",)

result_persistent = True
task_result_expires = None
send_events = True
enable_utc = True

task_serializer = 'json'
result_serializer = 'json'

accept_content = ['json']
timezone = 'America/New_York'
redis_max_connections = 10


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
