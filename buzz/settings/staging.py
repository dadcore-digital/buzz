from .base import *  # noqa: F403
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False
ALLOWED_HOSTS = ['api-staging.beegame.gg']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')

SECURE_SSL_REDIRECT = True

USE_X_FORWARDED_HOST = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'buzz_staging',
        'USER': 'buzz_staging',
        'PASSWORD': get_secret('DB_PASSWORD'),  # noqa: F405
        'HOST': '',
        'OPTIONS': {
                'init_command': 'SET storage_engine=INNODB'
        }
    }
}

STATIC_ROOT = '/home/ianfitzpatrick/apps/buzz_staging_static'
MEDIA_ROOT = '/home/ianfitzpatrick/apps/buzz_staging_media'

# Releases
try:
    import git
    repo = git.Repo(search_parent_directories=True)
    RELEASE_ID = repo.head.object.hexsha
except:
    RELEASE_ID = ''

sentry_sdk.init(
    dsn="https://8deb6f8290ac4c1e9e3b257d657386ec@o541952.ingest.sentry.io/5669400",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    release=RELEASE_ID
)
