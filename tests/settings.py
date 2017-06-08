import os
from celery import Celery

ADMINS = ()
DATABASES = {}


database_implementation = os.getenv('DATABASE', 'sqlite3')

DATABASES['default'] = {
    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django_atomic_signals.db',
    },
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': os.getenv('DATABASE_USER', 'postgres'),
        'NAME': 'djac',
    },
}[database_implementation]

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_DATABASE = int(os.getenv('REDIS_DATABASE', '0'))
BROKER_URL = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DATABASE)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

SECRET_KEY = '_uobce43e5osp8xgzle*yag2_16%y$sf*5(12vfg25hpnxik_*'

INSTALLED_APPS = (
    'django_atomic_celery',
    'tests',
    'django_nose',
)

DEBUG = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--verbosity=2', '--detailed-errors', '--rednose']

celery_app = Celery('django_atomic_celery')
celery_app.config_from_object('django.conf:settings')
