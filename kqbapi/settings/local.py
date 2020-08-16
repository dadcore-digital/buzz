from .base import *  

ALLOWED_HOSTS = ['kqbapi.local']
DEBUG = True
INTERNAL_IPS = ('127.0.0.1', '192.168.56.2', '192.168.56.1', '192.168.56.2')

STATIC_ROOT = '/var/www/kqbapi_static/'
MEDIA_ROOT = '/var/www/kbapi_media/'

INSTALLED_APPS = INSTALLED_APPS + [
    'django_extensions',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kqbapi',
        'USER': 'kqbapi',
        'PASSWORD': get_secret('DB_PASSWORD'),  # noqa: F405
        'HOST': '127.0.0.1',
        'OPTIONS': {
                'init_command': 'SET storage_engine=INNODB'
        }
    }
}