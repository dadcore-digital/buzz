from .base import *  

ALLOWED_HOSTS = ['buzz.local']
DEBUG = True
INTERNAL_IPS = ('127.0.0.1')
CI = True

STATIC_ROOT = '/var/www/buzz_static/'
MEDIA_ROOT = '/var/www/buzz_media/'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

