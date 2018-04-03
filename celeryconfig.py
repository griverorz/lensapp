from __future__ import absolute_import

broker_url = 'redis://redis:6379/0'
result_backend = 'redis://redis:6379/0'

result_persistent = True
task_result_expires = None
send_events = True
imports = ("lensapp.tasks",)
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True
redis_max_connections = 10
