from __future__ import absolute_import

broker_url = 'amqp://guest:guest@rabbitmq:5672//'
result_backend = "mongodb"

mongodb_backend_settings = {
    "host": "mongodb",
    "port": 27017,
    "database": "restdb",
    "taskmeta_collection": "taskcollection"
}

result_persistent = False
task_result_expires = None
send_events = True
imports = ("lensapp.tasks",)
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'America/New_York'
enable_utc = True
redis_max_connections = 10
