"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import dotenv_values

env = dotenv_values(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get("SECRET_KEY", "change-me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(env.get("DEBUG", 1)))

ALLOWED_HOSTS = [h.strip() for h in env.get("ALLOWED_HOSTS", "*").split(",") if h.strip()]

# Configuração Celery
CELERY_BROKER_URL = env.get("CELERY_BROKER_URL")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Log
    'reversion',

    # Import Export
    'import_export',

    # API
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',

    # Utils
    'utils.desk',
    'utils.mk',
    'utils.goon',
    'utils.telegram',
    'utils.mkat',
    # 'utils.avin',
    # 'utils.cronos',

    # APP
    'app.cancelamento',
    'app.ordem_servico',
    'app.movimentacao',
    'app.faturamento',
    # 'app.autonoc',
    # 'app.dashboard',
    # 'app.goontodesk',
    # 'app.ost',
    # 'app.spc',
    # 'app.x9',
]

MIDDLEWARE = [
    # arquivos estaticos modo produção
    'whitenoise.middleware.WhiteNoiseMiddleware',

    # Log
    'reversion.middleware.RevisionMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.get("POSTGRES_DB", "change-me"),
        'USER': env.get("POSTGRES_USER", "change-me"),
        'PASSWORD': env.get("POSTGRES_PASSWORD", "change-me"),
        'HOST': env.get("POSTGRES_HOST", "change-me"),
        'PORT': env.get("POSTGRES_PORT", "change-me"),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
str_pass_django = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': f'{str_pass_django}.UserAttributeSimilarityValidator',
    },
    {
        'NAME': f'{str_pass_django}.MinimumLengthValidator',
    },
    {
        'NAME': f'{str_pass_django}.CommonPasswordValidator',
    },
    {
        'NAME': f'{str_pass_django}.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Fortaleza'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'assets')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
