from django import forms
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from allauth.account.forms import SignupForm, LoginForm
from captcha.fields import CaptchaField


class CustomSignupForm(SignupForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']

    def clean_email(self):
        email = super().clean_email()
        # Генерация username
        email_prefix = email.split('@')[0]
        random_string = get_random_string(length=5)
        username = f"{email_prefix}_{random_string}"

        while User.objects.filter(username=username).exists():
            random_string = get_random_string(length=5)
            username = f"{email_prefix}_{random_string}"

        self.cleaned_data['username'] = username
        return email

    # def clean_email(self):
    #     email = super().clean_email()
    #     # Генерируем username здесь
    #     email_prefix = email.split('@')[0]
    #     random_string = get_random_string(length=5)
    #     username = f"{email_prefix}_{random_string}"
    #
    #     while User.objects.filter(username=username).exists():
    #         random_string = get_random_string(length=5)
    #         username = f"{email_prefix}_{random_string}"

        # Устанавливаем username
        self.cleaned_data['username'] = username
        return email


class CustomLoginForm(LoginForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле для кода
        if 'code' in self.fields:
            self.fields.pop('code')