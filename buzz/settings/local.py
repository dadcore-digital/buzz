from .base import *  

ALLOWED_HOSTS = ['buzz.local']
DEBUG = True
DEBUG_TOOLBAR = False
INTERNAL_IPS = ('127.0.0.1', '192.168.56.2', '192.168.56.1', '192.168.56.2')

STATIC_ROOT = '/var/www/buzz_static/'
MEDIA_ROOT = '/var/www/buzz_media/'

REQUEST_TIME_DELAY = 0

# INSTALLED_APPS += [
#     'debug_toolbar'
# ]
# Session Settings
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"

# Select 2 Autocomplete Settings
SELECT2_CACHE_BACKEND = "select2"

# MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

INSTALLED_APPS += [
    'django_extensions'
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'buzz',
        'USER': 'buzz',
        'PASSWORD': get_secret('DB_PASSWORD'),  # noqa: F405
        'HOST': '127.0.0.1',
        'OPTIONS': {
                'init_command': 'SET storage_engine=INNODB;',
                'charset': 'utf8mb4',
                'use_unicode': True                
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
    'select2': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SHELL_PLUS_IMPORTS = [
    'from buzz.tests.factories import *',
    'from casters.tests.factories import *',
    'from players.tests.factories import *',
    'from leagues.tests.factories import *',
    'from teams.tests.factories import *',
    'from matches.tests.factories import *'
]
