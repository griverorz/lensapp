from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from celery import Celery
from .tasks import process_image
from .config import ProdConfig
import os


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

app.config.from_object(ProdConfig)


def make_celery(app):
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_BROKER_URL'],
                    broker=app.config['CELERY_RESULT_BACKEND'])
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


########## Application ##########


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
        task = process_image.delay(filename)
        return({},
               202,
               {'Location': api.url_for(ConsumeImg,
                                        taskid=task.id)})

    @auth.login_required
    def get(self, taskid):
        task = process_image.AsyncResult(taskid)
        if task.state == 'PENDING':
            response = {
                'id': task.id,
                'state': task.state,
                'status': "Task has not started"
            }
        elif task.state != 'FAILURE':
            response = {
                'id': task.id,
                'state': task.state,
                'status': 'Task has exited',
                'result': task.info
            }
        else:
            response = {
                'id': task.id,
                'state': task.state,
                'status': str(task.info)
            }
        return(response, 200)


api.add_resource(ConsumeImg, '/api/v1.0/upload', endpoint='upload')
api.add_resource(ConsumeImg, '/api/v1.0/task/<string:taskid>', endpoint='task')


if __name__ == '__main__':
    app.run()
