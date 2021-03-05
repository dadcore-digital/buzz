from .base import *  

ALLOWED_HOSTS = ['buzz.local']
DEBUG = True
INTERNAL_IPS = ('127.0.0.1')

STATIC_ROOT = '/var/www/buzz_static/'
MEDIA_ROOT = '/var/www/buzz_media/'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'buzz',
        'USER': 'buzz',
        'PASSWORD': get_secret('DB_PASSWORD'),  # noqa: F405
        'HOST': '127.0.0.1',
        'OPTIONS': {
                'init_command': 'SET storage_engine=INNODB'
        }
    }
}