from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from celery import Celery
from .tasks import process_image
import os


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


app.config.update(
    CELERY_BROKER_URL='redis://redis:6379/0',
    CELERY_RESULT_BACKEND='redis://redis:6379/0',
    UPLOAD_FOLDER="."
)


def make_celery(app):
    celery = Celery(app.import_name,
                    backend='redis://redis:6379/0',
                    broker='redis://redis:6379/0')
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)

USER_DATA = {
    "admin": "pwd"
}


celery = make_celery(app)


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return(False)
    return(USER_DATA.get(username) == password)


class ConsumeImg(Resource):
    @auth.login_required
    def post(self):
        file = request.files['picture']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = process_image.delay(filename)
        return({"data": img.get()}, 200)


api.add_resource(ConsumeImg, '/upload')


if __name__ == '__main__':
    app.run()
