"""
Django settings for config project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde backend/.env (desarrollo local)
load_dotenv(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    os.environ.get('SECRET_KEY', 'django-insecure-parlia-dev-key-change-in-production-2026'),
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get(
    'DJANGO_DEBUG',
    os.environ.get('DEBUG', 'True'),
).lower() in ('true', '1', 'yes')


# 1. ALLOWED_HOSTS: Acepta el dominio de Render (.onrender.com, RENDER_EXTERNAL_HOSTNAME) y variables de entorno
_default_hosts = 'localhost,127.0.0.1,.onrender.com'
_raw_hosts = os.environ.get(
    'DJANGO_ALLOWED_HOSTS',
    os.environ.get('ALLOWED_HOSTS', _default_hosts),
)
ALLOWED_HOSTS = [host.strip() for host in _raw_hosts.split(',') if host.strip()]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    # Local PARLIA domain apps
    'apps.accounts.apps.AccountsConfig',
    'apps.learning.apps.LearningConfig',
    'apps.activities.apps.ActivitiesConfig',
    'apps.progress.apps.ProgressConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# 2. Database: Credenciales de MySQL externo leídas desde os.environ.get(...)
_db_options = {
    'charset': 'utf8mb4',
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
}

if os.environ.get('DB_SSL_CA'):
    _db_options['ssl'] = {'ca': os.environ.get('DB_SSL_CA')}
elif os.environ.get('DB_SSL', 'False').lower() in ('true', '1', 'yes'):
    _db_options['ssl'] = {}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', os.environ.get('MYSQL_DATABASE', 'parlia_db')),
        'USER': os.environ.get('DB_USER', os.environ.get('MYSQL_USER', 'root')),
        'PASSWORD': os.environ.get('DB_PASSWORD', os.environ.get('MYSQL_PASSWORD', '')),
        'HOST': os.environ.get('DB_HOST', os.environ.get('MYSQL_HOST', '127.0.0.1')),
        'PORT': os.environ.get('DB_PORT', os.environ.get('MYSQL_PORT', '3306')),
        'OPTIONS': _db_options,
    }
}


# Password validation

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


# Internationalization

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'


# 3. CORS (django-cors-headers) & CSRF para permitir peticiones desde la URL del frontend en Vue
_default_cors = 'http://localhost:5173,http://127.0.0.1:5173'
_frontend_url = os.environ.get('FRONTEND_URL', '').strip().rstrip('/')
_raw_cors = os.environ.get('CORS_ALLOWED_ORIGINS', _default_cors)

CORS_ALLOWED_ORIGINS = [
    origin.strip().rstrip('/')
    for origin in _raw_cors.split(',')
    if origin.strip()
]

if _frontend_url and _frontend_url not in CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS.append(_frontend_url)

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = list(CORS_ALLOWED_ORIGINS)
if RENDER_EXTERNAL_HOSTNAME:
    _render_origin = f"https://{RENDER_EXTERNAL_HOSTNAME}"
    if _render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_render_origin)

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'


# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'EXCEPTION_HANDLER': 'config.exceptions.custom_exception_handler',
}


# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
