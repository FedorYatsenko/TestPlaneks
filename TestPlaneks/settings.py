import os

from pathlib import Path

import django_heroku


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False

ALLOWED_HOSTS = ['test-planeks.herokuapp.com', '.localhost', '127.0.0.1']


# AWS S3 SETTINGS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"
AWS_DEFAULT_ACL = None
AWS_S3_REGION_NAME = 'us-east-2'
AWS_S3_SIGNATURE_VERSION = 's3v4'


# Application definition

INSTALLED_APPS = [
    'datasets.apps.DatasetsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
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

ROOT_URLCONF = 'TestPlaneks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'TestPlaneks.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

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


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

# PUBLIC_MEDIA_LOCATION = 'public'
# MEDIA_URL = f"{AWS_URL}/{PUBLIC_MEDIA_LOCATION}"
# DEFAULT_FILE_STORAGE = 'hello_django.storage_backends.PublicMediaStorage'

PRIVATE_MEDIA_LOCATION = 'private'
PRIVATE_FILE_STORAGE = 'TestPlaneks.storage_backends.PrivateMediaStorage'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Auth
LOGIN_REDIRECT_URL = 'home'


# Celery Configuration Options
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 15 * 60


# Activate Django-Heroku.
django_heroku.settings(locals())
