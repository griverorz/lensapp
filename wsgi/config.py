CELERY_BROKER = 'amqp://guest@127.0.0.1:5672//'


class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    DBNAME = "pdb"
    DBHOST = "localhost"
    DBPORT = "5432"
    DBUSER = "gonzalorivero"


class Prod(Config):
    DEBUG = False
    DEVELOPMENT = False
    DBNAME = "pdb"
    DBHOST = "localhost"
    DBPORT = "5432"
    DBUSER = "gonzalorivero"
    APP_HOST = "ec2-54-89-128-61.compute-1.amazonaws.com"
    APP_KEY = "/Users/gonzalorivero/.ssh/aws.pem"


