from allauth.account.views import SignupView, LoginView
from .forms import CustomSignupForm, CustomLoginForm
from django.shortcuts import render
from django.contrib import messages
from allauth.account.models import EmailAddress


class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        # Создаем пользователя
        self.user = form.save(self.request)

        # Отправляем письмо подтверждения
        email_address = EmailAddress.objects.add_email(
            self.request,
            self.user,
            form.cleaned_data["email"],
            confirm=True
        )

        # Сообщение пользователю
        messages.info(
            self.request,
            "Письмо с подтверждением отправлено на ваш email. "
            "Пожалуйста, проверьте почту и перейдите по ссылке для завершения регистрации."
        )

        return render(self.request, 'account/verification_sent.html', {
            'email': form.cleaned_data['email']
        })


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'


def index(request):
    return render(request, 'accounts/test.html')