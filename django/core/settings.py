"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os
import ast

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

if not DEBUG:
    # converting string to list
    ALLOWED_HOSTS = ast.literal_eval(os.environ.get('ALLOWED_HOSTS'))
else:
    ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'task1',
    'task2',
    'task3',
    'main',
    # 'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        # Get port from environment or default to 5432.
        'PORT': os.environ.get('DB_PORT', 5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

# USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# This setting defines the base URL to serve static files from. In this case, it specifies that static files will be
# served from the "/static/" URL. For example, if you have a CSS file named "styles.css" in your static files
# directory, it will be accessible at "/static/styles.css".
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = 'static/'

# This setting specifies additional directories where Django will look for static files. In the provided code,
# it indicates that the "static" directory within the project's base directory (BASE_DIR) should be considered for
# static files. You can add more directories to this list if you have multiple locations for static files.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# This setting defines the base URL to serve media files from. 
# In this case, it specifies that media files will be served from the "/images/" URL. 
# For example, if you have an uploaded image named "example.jpg", it will be accessible at "/images/example.jpg".
MEDIA_URL = '/'

# This setting specifies the absolute filesystem path to the directory where media files will be uploaded and stored. 
# In the provided code, it points to the "images" directory within the "static" directory.
MEDIA_ROOT = BASE_DIR / 'static'

# docker runs redis while local runs rabbit mq (redis is not working)
if not DEBUG:
    print('running redis')
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
else:
    # local runs on rabbitmq and does not need config
    print('running rabbitmq')
    pass

# gmail_send/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

CELERY_BEAT_SCHEDULE = {
    "scheduled_task": {
        "task": "task1.tasks.add",
        "schedule": 5.0,
        "args": (50, 180),
    },
    "database": {
        "task": "task3.tasks.bkup",
        "schedule": 5.0,
    },
}


""" crontab() Execute every minute.

crontab(minute=0, hour=0) Execute daily at midnight.

crontab(minute=0, hour='*/3') Execute every three hours: midnight, 3am, 6am, 9am, noon, 3pm, 6pm, 9pm.

crontab(minute=0, hour='0,3,6,9,12,15,18,21') Same as previous.

crontab(minute='*/15') Execute every 15 minutes.

crontab(day_of_week='sunday') Execute every minute (!) at Sundays.

crontab(minute='*', hour='*', day_of_week='sun') Same as previous.

crontab(minute='*/10', hour='3,17,22', day_of_week='thu,fri') Execute every ten minutes, but only between 3-4 am, 5-6 pm, and 10-11 pm on Thursdays or Fridays.

crontab(minute=0, hour='*/2,*/3') Execute every even hour, and every hour divisible by three. This means: at every hour except: 1am, 5am, 7am, 11am, 1pm, 5pm, 7pm, 11pm

crontab(minute=0, hour='*/5') Execute hour divisible by 5. This means that it is triggered at 3pm, not 5pm (since 3pm equals the 24-hour clock value of “15”, which is divisible by 5).

crontab(minute=0, hour='*/3,8-17') Execute every hour divisible by 3, and every hour during office hours (8am-5pm).

crontab(0, 0, day_of_month='2') Execute on the second day of every month.

crontab(0, 0, day_of_month='2-30/2') Execute on every even numbered day.

crontab(0, 0, day_of_month='1-7,15-21') Execute on the first and third weeks of the month.

crontab(0, 0, day_of_month='11', month_of_year='5') Execute on the eleventh of May every year.

crontab(0, 0, month_of_year='*/3') Execute every day on the first month of every quarter.

"""
