from celery.task import task
import time
from matplotlib.image import imread


@task
def process_image(x):
    img = imread(x)
    # some long running task here
    time.sleep(5)
    return(img.shape)
