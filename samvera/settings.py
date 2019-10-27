"""
Django settings for samvera project.

Based on 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import posixpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '980e51a4-86f5-41f6-9887-017b09fd5032'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True   

ALLOWED_HOSTS = ['www.komerist.ru', '212.220.110.23', '0.0.0.0', '192.168.0.10', '192.168.0.11', '192.168.0.12', '127.0.0.1', 'local.site.my', '192.168.0.99']

# EMAIL settings
from samvera import EMAIL_settings as ES
DEFAULT_FROM_EMAIL = ES.DEFAULT_FROM_EMAIL
EMAIL_HOST = ES.EMAIL_HOST
EMAIL_PORT = ES.EMAIL_PORT
EMAIL_HOST_USER = ES.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = ES.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = ES.EMAIL_USE_TLS

CART_SESSION_ID = "cart" # Ключ для хранения корзины в сессии пользователя

# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'smart_selects',
    #'nested_inline',
    'cart',
    #'shop',
    'app',
    'orders',
    'admin_reorder',
]

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]
ADMIN_REORDER = (
    'shop',
    {'app': 'app', 'label': 'Склад',
    'models': ('app.Tovar', 'app.Variaciya', 'app.Gallery')},

    {'app': 'app', 'label': 'Заказы',
    'models': ('app.Orders', 'app.OrderTovary', 'app.OrderTovaryVariaciya')},

    {'app': 'auth', 'label': 'Авторизация',
    'models': ('auth.User', 'auth.Group')},
#    # Keep original label and models
#    'sites', 

#    # Rename app
#    {'app': 'auth', 'label': 'Authorisation'},

#    # Reorder app models
#    {'app': 'auth', 'models': ('auth.User', 'auth.Group')},

#    # Exclude models
#    {'app': 'auth', 'models': ('auth.User', )},

#    # Cross-linked models
#    {'app': 'auth', 'models': ('auth.User', 'sites.Site')},

#    # models with custom name
#    {'app': 'auth', 'models': (
#        'auth.Group',
#        {'model': 'auth.User', 'label': 'Staff'},
#    )},
)

ROOT_URLCONF = 'samvera.urls'

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
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
            ],
        },
    },
]

WSGI_APPLICATION = 'samvera.wsgi.application'
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = [
    'app.auth.EmailAuthBackend',
]

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

USE_DJANGO_JQUERY = True
#JQUERY_URL = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['app/static']))

MEDIA_URL = '/media/'
MEDIA_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['app/media']))