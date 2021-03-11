from .base import *  

ALLOWED_HOSTS = ['buzz.local']
DEBUG = True
INTERNAL_IPS = ('127.0.0.1', '192.168.56.2', '192.168.56.1', '192.168.56.2')

STATIC_ROOT = '/var/www/buzz_static/'
MEDIA_ROOT = '/var/www/buzz_media/'

REQUEST_TIME_DELAY = 0

INSTALLED_APPS += [
    'debug_toolbar'
]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

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

SHELL_PLUS_IMPORTS = [
    'from buzz.tests.factories import *',
    'from players.tests.factories import *',
    'from leagues.tests.factories import *',
    'from teams.tests.factories import *',
    'from matches.tests.factories import *'
]
