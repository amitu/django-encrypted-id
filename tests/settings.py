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
    "testapp.testapp",
    "django.contrib.contenttypes"
)

ROOT_URLCONF = "testapp.urls"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": ["django.contrib.auth.context_processors.auth"]
        },
    }
]
