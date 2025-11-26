from pathlib import Path

from config import BASE_DIR
from config import env

APPS_DIR = BASE_DIR / "apps"
PROJECT_DIR = BASE_DIR / "config"
FRONTEND_DIR = BASE_DIR / "frontend"

# ==========================
# Core Django Settings
# ==========================

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# ==========================
# Application Definition
# ==========================

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_cleanup.apps.CleanupConfig",
    "django_extensions",
    "admin_honeypot",
]

LOCAL_APPS = [
    "apps.visits.apps.VisitsConfig",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# ==========================
# Middleware Configuration
# ==========================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==========================
# URL Configuration
# ==========================

ROOT_URLCONF = "config.urls"

# ==========================
# Template Configuration
# ==========================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==========================
# WSGI Configuration
# ==========================

WSGI_APPLICATION = "config.wsgi.application"

# ==========================
# Database Configuration
# ==========================
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==========================
# Cache Configuration
# ==========================
# https://docs.djangoproject.com/en/dev/ref/settings/#caches

CACHES = {
    "default": env.cache(
        "DJANGO_CACHE_URL", default="locmem://unique-snowflake"
    )
}

# ==========================
# Password Validation
# ==========================
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 12,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ==========================
# Internationalization
# ==========================
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIME_ZONE = "UTC"

# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# ==========================
# Static Files (CSS, JavaScript, Images)
# ==========================
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url

STATIC_URL = "/static/"

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = BASE_DIR / "staticfiles"

# https://docs.djangoproject.com/en/dev/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = [BASE_DIR / "static"]

# ==========================
# Media Files
# ==========================
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root

MEDIA_ROOT = Path(env("DJANGO_MEDIA_ROOT", default=str(BASE_DIR / "media")))

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# ==========================
# Security Settings
# ==========================

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# ==========================
# Custom Settings
# ==========================

# Blacklist for username registration
ACCOUNT_USERNAME_BLACKLIST = [
    "admin",
    "superuser",
    "root",
    "webmaster",
    "theboss",
    "administrator",
    "support",
    "help",
    "system",
]
