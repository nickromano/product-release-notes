import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ENVIRONMENT_LOCAL = 'local'
ENVIRONMENT_HEROKU = 'heroku'

ENVIRONMENT = os.environ.get('ENVIRONMENT', ENVIRONMENT_LOCAL)

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', '*')]
DEBUG = os.environ.get('DEBUG', ENVIRONMENT == ENVIRONMENT_LOCAL)
SECRET_KEY = os.environ.get('SECRET_KEY', '123')

if ENVIRONMENT == ENVIRONMENT_LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test'
        }
    }
elif ENVIRONMENT == ENVIRONMENT_HEROKU:
    # Running in Heroku
    import dj_database_url  # noqa
    db_from_env = dj_database_url.config()  # noqa
    DATABASES = {
        'default': db_from_env
    }
else:
    raise Exception(
        '{} not a valid ENVIRONMENT option.'.format(ENVIRONMENT)
    )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',

    'product_release_notes'
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        }
    },
]

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = []

if ENVIRONMENT == ENVIRONMENT_HEROKU:
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
