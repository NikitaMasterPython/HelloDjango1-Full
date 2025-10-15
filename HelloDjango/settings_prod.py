from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['195.42.234.138', 'bill.ufo.hosting']

# Оставляем SQLite - все работает!
# DATABASES остается как в settings.py

# Статические файлы
STATIC_ROOT = '/home/django/HelloDjango1-Full/staticfiles'
MEDIA_ROOT = '/home/django/HelloDjango1-Full/media'

# Отключаем подтверждение почты временно
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Безопасность
CSRF_TRUSTED_ORIGINS = [
    'http://195.42.234.138',
    'https://195.42.234.138', 
    'http://bill.ufo.hosting',
    'https://bill.ufo.hosting'
]

# Обновляем настройки allauth
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*']
# Временно оставляем вывод в консоль
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.yandex.ru'
#EMAIL_PORT = 587  # ИСПРАВИЛИ: 587 вместо 465
#EMAIL_USE_TLS = True  # ИСПРАВИЛИ: TLS вместо SSL
#EMAIL_HOST_USER = 'therussiansaga@yandex.ru'
#EMAIL_HOST_PASSWORD = ''  # обычный пароль от ящика
#№DEFAULT_FROM_EMAIL = 'therussiansaga@yandex.ru'
# Но включаем подтверждение почты чтобы видеть что работает
ACCOUNT_EMAIL_VERIFICATION = 'none'
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Меняем домен с example.com на твой
SITE_ID = 1
