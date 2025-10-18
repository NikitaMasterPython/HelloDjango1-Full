from allauth.account.views import SignupView, LoginView
from .forms import CustomSignupForm, CustomLoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from allauth.account.models import EmailAddress
from allauth.account import signals  # Добавлен импорт signals
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        # Проверяем существование пользователя
        if User.objects.filter(email__iexact=email).exists():
            messages.error(
                self.request,
                "Пользователь с таким email уже существует. "
                "Пожалуйста, используйте другой email или восстановите пароль."
            )
            return self.form_invalid(form)

        # Создаем пользователя
        self.user = form.save(self.request)

        # Отправляем письмо подтверждения
        email_address = EmailAddress.objects.add_email(
            self.request,
            self.user,
            email,
            confirm=True
        )
        # ОТПРАВКА ПИСЬМА ДО ОТПРАВКИ СИГНАЛА
       # email_address.send_confirmation()

        # Отправляем сигнал о регистрации
        signals.user_signed_up.send(
            sender=self.user.__class__,
            request=self.request,
            user=self.user
        )

        # Сообщение пользователю
        return render(self.request, 'account/verification_sent.html', {
            'email': email
        })

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'

def index(request):
    return render(request, 'accounts/test.html')
