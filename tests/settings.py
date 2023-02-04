import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEBUG = True

SECRET_KEY = "3qmq&fh=^fl-*a9e82uj$kyj8=0)2s9@n4j^@y6qa=p#^fzcco"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    "tests.testapp",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.staticfiles"
)

ROOT_URLCONF = "tests.urls"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": ["django.contrib.auth.context_processors.auth"]
        },
    }
]
