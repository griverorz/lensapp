from celery.task import task
import time
from matplotlib.image import imread


@task
def process_image(x):
    img = imread(x)
    time.sleep(25)
    return(img.shape)
