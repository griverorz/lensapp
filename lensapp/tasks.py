from celery.task import task
import time


@task
def process_image():
    # some long running task here
    time.sleep(5)
    return(True)
