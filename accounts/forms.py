from django import forms
from django.urls import path, include
from allauth.account.forms import SignupForm, LoginForm
# from captcha.fields import ReCaptchaField


from captcha.fields import CaptchaField
# from django_recaptcha.fields import ReCaptchaField

# from django_recaptcha.fields import ReCaptchaField
from django.utils.crypto import get_random_string

from allauth.account.forms import SignupForm
from django import forms
from django.utils.crypto import get_random_string
# from captcha.fields import ReCaptchaField
from django.contrib.auth.models import User

class CustomSignupForm(SignupForm):
    # captcha = ReCaptchaField()
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Удаляем поле username из формы
        if 'username' in self.fields:
            del self.fields['username']

    def save(self, request):
        # Получаем пользователя через родительский метод
        user = super().save(request)

        # Генерируем уникальное имя пользователя на основе email
        email_prefix = self.cleaned_data['email'].split('@')[0]
        random_string = get_random_string(length=5)
        new_username = f"{email_prefix}_{random_string}"

        # Убедимся, что имя уникально
        while User.objects.filter(username=new_username).exists():
            random_string = get_random_string(length=5)
            new_username = f"{email_prefix}_{random_string}"

        # Обновляем имя пользователя
        user.username = new_username
        user.save()

        # Отправляем письмо подтверждения
        from allauth.account.models import EmailAddress
        email_address = EmailAddress.objects.add_email(
            request,
            user,
            self.cleaned_data["email"],
            confirm=True
        )

        return user

class CustomLoginForm(LoginForm):
    # captcha = ReCaptchaField()
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле для кода
        self.fields.pop('code', None)
        self.login_by_code = False






# class CustomSignupForm(SignupForm):
#     captcha = ReCaptchaField()
#
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Убираем ненужные поля
#         self.fields.pop('password2', None)

    # def save(self, request):
    #     # Дополнительная логика при сохранении пользователя
    #     user = super().save(request)
    #     return user


# class CustomLoginForm(LoginForm):
#     captcha = ReCaptchaField()
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Убедимся, что используется только пароль
#         self.fields.pop('code', None)  # Удаляем поле для кода, если оно есть

# class CustomLoginForm(LoginForm):
#     captcha = ReCaptchaField()
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Убираем поле для кода
#         self.fields.pop('code', None)