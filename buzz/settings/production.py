from .base import *  # noqa: F403
DEBUG = True
ALLOWED_HOSTS = ['kqb.buzz']

DEBUG = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')

SECURE_SSL_REDIRECT = True

USE_X_FORWARDED_HOST = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'buzz',
        'USER': 'buzz',
        'PASSWORD': get_secret('DB_PASSWORD'),  # noqa: F405
        'HOST': '',
        'OPTIONS': {
                'init_command': 'SET storage_engine=INNODB'
        }
    }
}

STATIC_ROOT = '/home/ianfitzpatrick/apps/buzz_static'
MEDIA_ROOT = '/home/ianfitzpatrick/apps/buzz_media'
