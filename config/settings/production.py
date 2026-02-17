from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'devamsizliktakip.info.tr', 
    'www.devamsizliktakip.info.tr', 
    '192.168.1.100',  # Sunucunuzun sabit IP'si
    'localhost', 
    '127.0.0.1'
]

# Production database (example with PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Security settings for production
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['https://devamsizliktakip.info.tr']