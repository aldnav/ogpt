"""
Django settings for ogpt project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
VAR_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, "var")
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "l&4!_ni_rzm58ev=fg%7t3ohpk!-@9k#hwbvl1ng8ds0h*s)^r"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.forms",
    "rest_framework",
    "django_tables2",
    "django_filters",
    "bootstrap4",
    "django_extensions",
    "apps.govproject",
    "apps.django_tables_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ogpt.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_ROOT, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
            ]
        },
    }
]

WSGI_APPLICATION = "ogpt.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# Change the DATABASES index on the right to appropriate values:
#    default: SQLite
#    postgre: PostgreSQL
#    mysql: MySQL
DB = "default"

DATABASES = {
    "default": {  # DEFAULT: SQLite
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    },
    "postgre": {  # PostgreSQL
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "dbase",  # Production Database Name
        "USER": "user",  # Database Username
        "PASSWORD": "pass",  # Database Password
        "HOST": "127.0.0.1",  # Database IP Address
        "PORT": "5432",  # Database Port (default: 5432)
        "TEST": {
            "NAME": "test",  # Test Database Name (Optional)
        },
    },
    "mysql": {  # MySQL
        "ENGINE": "django.db.backends.mysql",
        "NAME": "dbase",  # Production Database Name
        "USER": "user",  # Database Username
        "PASSWORD": "pass",  # Database Password
        "HOST": "127.0.0.1",  # Database IP Address
        "PORT": "3306",  # Database Port (default: 3306)
        "TEST": {
            "NAME": "test",  # Test Database Name (Optional)
        },
    },
}

DATABASES["default"] = DATABASES[DB]

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static"),)
STATIC_ROOT = os.path.join(VAR_ROOT, "staticserve")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(VAR_ROOT, "media")
MEDIA_URL = "/media/"

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# django_tables2
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"


# Anonymous/Ghost/Dummy user
ANONYMOUS_USER = 1

# STAFF USER DATA
STAFF_USER_DATA = [
    # email, username, first name, last name, password
    ('aldrin@ogpt.com', 'aldrin', 'Aldrin', 'Navarro', 'aldrin'),
]

SITE_ID = 1

# @NOTE: Migrate to directory settings in the future
try:
    from .dev_settings import *
except ImportError:
    pass
