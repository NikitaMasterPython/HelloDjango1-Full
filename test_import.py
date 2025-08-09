
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HelloDjango.settings')
django.setup()

from captcha.fields import ReCaptchaField
print("Импорт успешен!")