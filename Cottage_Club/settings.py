"""
Django settings for Cottage_Club project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o6okuy7tws(_)=n!$38+w37tkr+qqqpt!@pqh-0#oyta7be09w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

MPTT_ADMIN_LEVEL_INDENT = 10
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'treebeard',
    'storages',
    'tinymce',
    'mptt',
    'Cottage_Club.main',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.tz',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    "%s/%s/" % (ROOT_PATH, 'templates'),
)

ROOT_URLCONF = 'Cottage_Club.urls'

WSGI_APPLICATION = 'Cottage_Club.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'transaction_hooks.backends.mysql',
        'NAME': 'CottageClub',
        'USER': 'pyuser',
        'PASSWORD': 'welcome',
        'HOST': '',
        'PORT': '3306',
    }
}

TINYMCE_JS_URL = 'https://tinymce.cachefly.net/4.0/tinymce.min.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "paste,searchreplace,table,link,code,autoresize,autosave",
    'custom_undo_redo_levels': 10,
    'relative_urls': False,
    'style_formats_merge': True,
    'style_formats': [
        {
            'title': "Languages",
            'items': [
                {'title': 'Bash', 'block': 'pre', 'classes': 'language-bash', 'attributes': {'data-lang': 'bash'}},
                {'title': 'Python', 'block': 'pre', 'classes': 'language-python', 'attributes': {'data-lang': 'python'}},
                {'title': 'Ruby', 'block': 'pre', 'classes': 'language-ruby', 'attributes': {'data-lang': 'ruby'}},
                {'title': 'PHP', 'block': 'pre', 'classes': 'language-php', 'attributes': {'data-lang': 'php'}},
                {'title': 'C#', 'block': 'pre', 'classes': 'language-csharp', 'attributes': {'data-lang': 'csharp'}},
                {'title': 'JS', 'block': 'pre', 'classes': 'language-javascript', 'attributes': {'data-lang': 'js'}},
                {'title': 'Java', 'block': 'pre', 'classes': 'language-java', 'attributes': {'data-lang': 'java'}},
                {'title': 'JSON', 'block': 'pre', 'classes': 'language-json', 'attributes': {'data-lang': 'json'}},
            ]
        },
        {
            'title': 'Spoiler', 'block': 'pre', 'classes': 'collapsable'
        }
    ]
}
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = '%s/../../static/' % ROOT_PATH

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
MEDIA_ROOT = '%s/../media/' % ROOT_PATH
DEFAULT_IMAGE = 'images/default_product.png'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'
STATICFILES_MAIN_DIR = '%s/static/' % ROOT_PATH
STATICFILES_DIRS = (
    STATICFILES_MAIN_DIR,
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)