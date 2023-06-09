"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from .db_settings import DEV_SECRET, DEV_DATABASES,AWS_SECRET

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DEV_SECRET['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['emo-ai.com', 'localhost', 'www.emo-ai.com','10.0.0.245', '127.0.0.1','13.124.49.231']
CSRF_TRUSTED_ORIGINS = ['https://emo-ai.com', 'https://www.emo-ai.com','https://0.0.0.0:8000']
# Application definition

INSTALLED_APPS = [
    'daphne',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webcam_app',
    'chartjs', #pip install django-chartjs
    'account',
    'post_comment',
    'django_ses'
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

ROOT_URLCONF = 'webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'webapp.wsgi.application'
ASGI_APPLICATION = "webapp.asgi.application" # 비동기 인터페이스 WEBSOCKET 통신을 위해 추가



# WEBSOCKET 통신을 위해 추가
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = DEV_DATABASES

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'account.User'

# AUTHENTICATION_BACKENDS = [

#     # Needed to login by username in Django admin, regardless of `allauth`
#     'django.contrib.auth.backends.ModelBackend',

#     # `allauth` specific authentication methods, such as login by e-mail
#     'allauth.account.auth_backends.AuthenticationBackend',

# ]

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
ROOT_DIR = os.path.dirname(BASE_DIR)

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [
    STATIC_DIR,
    ]
STATIC_ROOT = os.path.join(BASE_DIR,'_static')

#MEDIA 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# EMAIL_BACKEND = AWS_SECRET['EMAIL_BACKEND']
# AWS_ACCESS_KEY_ID = AWS_SECRET['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = AWS_SECRET['AWS_SECRET_ACCESS_KEY']
# AWS_SES_REGION_NAME = AWS_SECRET['AWS_SES_REGION_NAME']
# AWS_SES_REGION_ENDPOINT = AWS_SECRET['AWS_SES_REGION_ENDPOINT']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = AWS_SECRET['AWS_SES_REGION_NAME']
EMAIL_HOST_USER = AWS_SECRET['AWS_ACCESS_KEY_ID']
EMAIL_HOST_PASSWORD =  AWS_SECRET['AWS_SECRET_ACCESS_KEY']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'bluewin92@naver.com'