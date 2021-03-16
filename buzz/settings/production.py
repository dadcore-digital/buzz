from .base import *  # noqa: F403
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False
ALLOWED_HOSTS = ['kqb.buzz', 'api.beegame.gg']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')

SECURE_SSL_REDIRECT = True

USE_X_FORWARDED_HOST = True

# Session Settings
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"

# Select 2 Autocomplete Settings
SELECT2_CACHE_BACKEND = "select2"

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


STATIC_ROOT = '/home/ianfitzpatrick/apps/buzz_static'
MEDIA_ROOT = '/home/ianfitzpatrick/apps/buzz_media'

# Releases
try:
    import git
    repo = git.Repo(search_parent_directories=True)
    RELEASE_ID = repo.head.object.hexsha
except:
    RELEASE_ID = ''

sentry_sdk.init(
    dsn="https://4dad2ef9e2e94a3aaec714b7138abd28@o541952.ingest.sentry.io/5660900",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    release=RELEASE_ID
)