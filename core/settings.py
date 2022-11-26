
import os
from django.contrib import messages
from pathlib import Path 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
 

# Read SECRET_KEY from an environment variable 
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')


#   OR

# Read secret key from a file
# with open('secret_key.txt') as f:
#     SECRET_KEY = f.read().strip()


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

# ALLOWED_HOSTS = [ "*" ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customauth',
    'shop',
    'accounts'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shop.middlewares.cart_middleware'
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


# Database 

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "modernman",
        "USER": "postgres",
        "PASSWORD": "sweetpoison",
        "HOST": "localhost",
        "client_encoding": "UTF8"
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




# Static files (CSS, JavaScript, Images) 
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "core/static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Deployment: path to the directory where collectstatic will collect static files for deployment.
# STATIC_ROOT = BASE_DIR/'static'

# The URL to use when referring to static files (where they will be served from)
# STATIC_URL = '/static/'

# media files
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"



# messages
MESSAGE_TAGS = {
    messages.ERROR: "danger",

}


LOGIN_URL = 'login'

if DEBUG:
    # email
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_HOST = 'smtp.domain.com'
    EMAIL_PORT = 587
    EMAIL_HOST_PASSWORD = "password"
    EMAIL_HOST_USER = "username"
    EMAIL_USE_TLS = True
    
    
    
# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },



    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_true']
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
        }
    },


    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,

        },
        'django.server': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,

        },
        'modernman_final.custom': {
            'handlers': ['file'],
            'formatter': 'verbose',
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'propagate': True,

        },
    },
}

# debug logging   is very verbose as it includes all database queries
DJANGO_LOG_LEVEL = DEBUG


# custom user model
AUTH_USER_MODEL = "customauth.CustomUser"
 
 
LOG_OUT_REDIRECT_URL = 'login'



# deploy on heroku
# import django_heroku
# django_heroku.settings(locals())


# deployment
SESSION_COOKIE_SECURE = True

# ALLOWED_HOSTS = ['web-production-3640.up.railway.app', '127.0.0.1'] 
ALLOWED_HOSTS = ['railway.com' 'web-production-3640.up.railway.app', '127.0.0.1'] 


## (replace the string below with your own site URL):
# CSRF_TRUSTED_ORIGINS = ['https://web-production-3640.up.railway.app']


# During development/for this tutorial you can instead set just the base URL
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app', 'https://127.0.0.1', 'http://127.0.0.1'] 



# Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

