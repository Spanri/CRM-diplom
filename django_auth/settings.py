import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'klc=#bj7qm#iiz%1ru-6y3%guc5_e(hq+3hm3&65dg6%c%@(*y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

from corsheaders.defaults import default_methods
# CORS_ORIGIN_WHITELIST = (
#     'http//:localhost:8080',
# )
CORS_ORIGIN_ALLOW_ALL = True

import boto3
from boto3.s3.transfer import S3Transfer

local_directory = 'media/'
transfer = S3Transfer(boto3.client('s3', 'your bucket region', 
                                   aws_access_key_id = '*********',
                                   aws_secret_access_key='********'))
client = boto3.client('s3')
bucket = 'edms-mtuci'
for root, dirs, files in os.walk(local_directory):
    for filename in files:
        local_path = os.path.join(root, filename)
        relative_path = os.path.relpath(local_path, local_directory)
        s3_path = os.path.join('your s3 path',relative_path)
        if filename.endswith('.pdf'):
            transfer.upload_file(local_path, bucket, s3_path,extra_args={'ACL': 'public-read'})
        else:
transfer.upload_file(local_path, bucket, s3_path)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'users',
    'docs',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'django_auth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'staticfiles')],
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

WSGI_APPLICATION = 'django_auth.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

# Для 
REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 
        'users.serializers.PasswordResetSerializer',
}


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# Для деплоймента
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/static/')
# STATIC_DIR = os.path.join(BASE_DIR, 'staticfiles/')
# STATIC_URL = 'staticfiles/'
STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, 'staticfiles/static/'),
    os.path.join(BASE_DIR, 'frontend/dist/'),
)
MEDIA_ROOT = os.path.join(BASE_DIR, '')
MEDIA_URL = '/'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    )
}

# SMTP сервер
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'edmsmtuci@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get("EDMS-MAIL-PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Для создания связей моделей в БД
AUTH_USER_MODEL = 'users.User'

# Хероку
import django_heroku
django_heroku.settings(locals())
