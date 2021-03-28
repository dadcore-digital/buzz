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
    if 'GET_SECRETS_FROM_ENV' in os.environ.keys():
        return os.environ[secret_name]

    else:
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
DEBUG_TOOLBAR = False
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'corsheaders',
    'django_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',    
    'allauth.socialaccount.providers.discord',
    'django_filters',
    'loginas',
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
    'staff',
    'api'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
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

SITE_ID = 1

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Login & Account Related
LOGIN_REDIRECT_URL = '/dispatch/'
ACCOUNT_MAX_EMAIL_ADDRESSES = 1
ACCOUNT_EMAIL_VERIFICATION = False

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Required by django admin interface
X_FRAME_OPTIONS='SAMEORIGIN'

STATICFILES_DIRS = [
    f'{str(Path(cwd).parent.parent)}/assets'
]

CORS_ALLOW_ALL_ORIGINS = True

# Django Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'api.paginators.StandardResultsSetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_VERSION': 1.0
}   


# Steam Settings
STEAM_GAME_ID = '663670'

# Streams/Twitch Settings
TWITCH_CLIENT_ID = get_secret('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = get_secret('TWITCH_CLIENT_SECRET')
TWITCH_GAME_ID = '506455'

# BGL
BGL_AUTH_HANDOFF_URL = 'https://league-beegame-gg.web.app'

NANOID_LIBRARY = '6789BCDFGHJKLMNPQRTWbcdfghjkmnpqrtwz'
