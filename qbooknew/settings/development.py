from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'quebook',
        'USER': 'malaka',
        'PASSWORD': 'malaka1999625',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login/'