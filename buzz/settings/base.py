import json
from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured


cwd = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = str(Path(cwd).parent)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))

def get_secret(secret_name):
    """
    Get secret variable or return explicit exception.

    Always return as string, not unicode.

    Must store this in base settings file due to structure of multiple
    settings files, or risk circular imports.
    """
    # Secrets file location
    secrets_file = f'{PROJECT_DIR}/settings/secrets.json'

    with open(secrets_file) as f:
        secrets_file = json.loads(f.read())
    try:
        return str(secrets_file[secret_name])

    except KeyError:
        error_msg = 'Missing secrets file.'
        raise Exception(error_msg)

SECRET_KEY = get_secret('SECRET_KEY')

DEBUG = True
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'django_filters',
    'buzz',
    'players',
    'leagues',
    'teams',
    'matches',
    'casters',
    'awards',
    'events',
    'streams',
    'beegame',
    'api',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'buzz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(Path(BASE_DIR).parents[1]) + '/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'buzz.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Required by django admin interface
X_FRAME_OPTIONS='SAMEORIGIN'

STATICFILES_DIRS = [
    f'{str(Path(cwd).parent.parent)}/assets'
]

# Django Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'api.paginators.StandardResultsSetPagination'
}

# Steam Settings
STEAM_GAME_ID = '663670'

# Streams/Twitch Settings
TWITCH_CLIENT_ID = get_secret('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = get_secret('TWITCH_CLIENT_SECRET')
TWITCH_GAME_ID = '506455'