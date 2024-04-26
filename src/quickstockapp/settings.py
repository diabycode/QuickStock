"""
Django settings for quickstockapp project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import json
import sys

from django.contrib.staticfiles import finders

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

try:
    with open(BASE_DIR / ".eVars.json") as env_file:
        ENV = json.load(env_file)
except FileNotFoundError:
    raise FileNotFoundError("Env vars file not found !")

SECRET_KEY = ENV.get("SECRET_KEY")
DEBUG = ENV.get("DEBUG")
ALLOWED_HOSTS = ENV.get("ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'stores',
    'products',
    'orders',
    'sales',
    'pwa',
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

ROOT_URLCONF = 'quickstockapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "base_templates",
            BASE_DIR / "quickstockapp/templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'stores.context_processors.stores'
            ],
        },
    },
]

WSGI_APPLICATION = 'quickstockapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.UserModel'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "base_staticfiles",
    BASE_DIR / "quickstockapp/static",
]

# PWA_SERVICE_WORKER_PATH = BASE_DIR / "quickstockapp/static/js/quickstockapp" / "serviceworker.js"
PWA_SERVICE_WORKER_PATH = finders.find("js/quickstockapp/serviceworker.js")
PWA_APP_NAME = 'QuickStock'
PWA_APP_DESCRIPTION = "QuickStock PWA"
# PWA_APP_THEME_COLOR = '#000000'
# PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/dashbord/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/icons/quickstockapp/logo150x150.png',
        'sizes': '150x150'
    },
    {
        'src': '/static/icons/quickstockapp/logo144x144.png',
        'sizes': '144x144'
    },
    {
        'src': '/static/icons/quickstockapp/logo225x225.png',
        'sizes': '225x225'
    },
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/icons/quickstockapp/logo150x150.png',
        'sizes': '150x150'
    },
    {
        'src': '/static/icons/quickstockapp/logo144x144.png',
        'sizes': '144x144'
    },
    {
        'src': '/static/icons/quickstockapp/logo225x225.png',
        'sizes': '225x225'
    },
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/icons/quickstockapp/logo22x22.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'fr-FR'