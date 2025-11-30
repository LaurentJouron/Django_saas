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
# Email Configuration
# ==========================
# Backend de messagerie
EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)

# Configuration SMTP
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)

# Identifiants
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

# Timeout (en secondes)
EMAIL_TIMEOUT = env.int("EMAIL_TIMEOUT", default=30)

# Configuration de l'expéditeur par défaut
DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER or "noreply@django_saas.com"
)
SERVER_EMAIL = env(
    "SERVER_EMAIL", default=EMAIL_HOST_USER or "server@django_saas.com"
)

# Administrateurs (pour les emails d'erreur Django)
ADMINS = [
    (
        env("ADMIN_USER_NAME", default="Laurent"),
        env("ADMIN_USER_EMAIL", default="laurentjouron@gmail.com"),
    ),
]
MANAGERS = ADMINS

# Configuration de validation (optionnel mais recommandé)
if EMAIL_USE_TLS and EMAIL_USE_SSL:
    raise ValueError(
        "EMAIL_USE_TLS et EMAIL_USE_SSL ne peuvent pas être activés simultanément"
    )

if EMAIL_USE_TLS and EMAIL_PORT not in [587, 25]:
    import warnings

    warnings.warn(f"Port {EMAIL_PORT} inhabituel pour TLS (recommandé: 587)")

if EMAIL_USE_SSL and EMAIL_PORT != 465:
    import warnings

    warnings.warn(f"Port {EMAIL_PORT} inhabituel pour SSL (recommandé: 465)")

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
    "apps.commando.apps.CommandoConfig",
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
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.visits.middleware.VisitMiddleware",
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
# Database Configuration (SOLIDE)
# ==========================

# Utilise DJANGO_DATABASE_URL si elle existe (production)
# ou SQLite par défaut (si non écrasé par dev.py)
DATABASES = {
    "default": env.db_url(
        "DJANGO_DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}

# ==========================
# Cache Configuration
# ==========================
# https://docs.djangoproject.com/en/dev/ref/settings/#caches

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}


# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

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

# Source folder for your static files during development
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Subfolder for vendors (Bootstrap, jQuery, etc.)
STATICFILES_VENDOR_DIR = STATIC_DIR / "vendors"

# Django will look for the static files in these folders
# https://docs.djangoproject.com/en/dev/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = [STATIC_DIR]

# Output folder for 'python manage.py collection'
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_ROOT.mkdir(parents=True, exist_ok=True)

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

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
