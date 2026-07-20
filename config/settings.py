"""
Django settings for config project.
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Load environment variables
load_dotenv(BASE_DIR / ".env")



# Security
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-development-key"
)


DEBUG = os.getenv(
    "DEBUG",
    "False"
) == "True"



# Hosts

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]


# Add deployed domain dynamically
DEPLOY_DOMAIN = os.getenv(
    "DEPLOY_DOMAIN"
)

if DEPLOY_DOMAIN:
    ALLOWED_HOSTS.append(
        DEPLOY_DOMAIN
    )



# CSRF trusted origins

CSRF_TRUSTED_ORIGINS = []


if DEPLOY_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(
        f"https://{DEPLOY_DOMAIN}"
    )



# Application definition

INSTALLED_APPS = [

    "django.contrib.admin",

    "django.contrib.auth",

    "django.contrib.contenttypes",

    "django.contrib.sessions",

    "django.contrib.messages",

    "django.contrib.staticfiles",


    "accounts",

    "projects",

    "agents",

]




MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",


    # WhiteNoise static files
    "whitenoise.middleware.WhiteNoiseMiddleware",


    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]




ROOT_URLCONF = "config.urls"




TEMPLATES = [

    {

        "BACKEND":
        "django.template.backends.django.DjangoTemplates",


        "DIRS": [
            BASE_DIR / "templates"
        ],


        "APP_DIRS": True,


        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

            ],

        },

    },

]




WSGI_APPLICATION = "config.wsgi.application"





# Database

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


if DATABASE_URL:

    DATABASES = {

        "default":
        dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600
        )

    }

else:

    DATABASES = {

        "default": {

            "ENGINE":
            "django.db.backends.sqlite3",

            "NAME":
            BASE_DIR / "db.sqlite3",

        }

    }





# Password validation

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },

]





# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True





# Static files

STATIC_URL = "/static/"


STATICFILES_DIRS = [

    BASE_DIR / "static"

]


STATIC_ROOT = BASE_DIR / "staticfiles"



# WhiteNoise compression

STORAGES = {

    "default": {

        "BACKEND":
        "django.core.files.storage.FileSystemStorage",

    },


    "staticfiles": {

        "BACKEND":
        "whitenoise.storage.CompressedManifestStaticFilesStorage",

    },

}





# Media

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"





# Authentication

LOGIN_URL = "/accounts/login/"

LOGIN_REDIRECT_URL = "/dashboard/"

LOGOUT_REDIRECT_URL = "/"





# Security for production

if not DEBUG:

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True