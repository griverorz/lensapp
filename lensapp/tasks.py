from celery.task import task
import time
from matplotlib.image import imread
import random


@task(bind=True, max_retries=5)
def process_image(self, x):
    try:
        img = imread(x)
        time.sleep(25)
        return(img.shape)
    except Exception as e:
        jittered = int(random.uniform(2, 4) ** self.request.retries)
        self.retry(exc=e, countdown=jittered)
