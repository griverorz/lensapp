from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug
from flask_httpauth import HTTPBasicAuth
from celery import Celery
import config
from tasks import process_image

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


def make_celery(app):
    celery = Celery(app.import_name, broker=config.CELERY_BROKER)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    return celery


USER_DATA = {
    "admin": "pwd"
}


celery = make_celery(app)
app.config.from_object('config')


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return(USER_DATA.get(username) == password)


class ConsumeImg(Resource):
    @auth.login_required
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('picture',
                           type=werkzeug.datastructures.FileStorage,
                           location='files')
        args = parse.parse_args()
        imgfile = args['picture']
        res = process_image.apply_async()
        if res:
            return({'filename': imgfile.filename}, 200)
        return(False)


api.add_resource(ConsumeImg, '/upload')


if __name__ == '__main__':
    app.run()


# curl -i -X POST -H "Content-Type: multipart/form-data" -F "picture=@Washington-DC-hero-H.jpeg" http://127.0.0.1:5000/upload --user admin:pwd

# celery -A app.celery worker --loglevel=info --config=celeryconfig
