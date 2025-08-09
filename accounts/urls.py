from django.urls import path
from .views import CustomSignupView, CustomLoginView
from allauth.account.views import LogoutView, PasswordResetView, PasswordResetDoneView

urlpatterns = [

    path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),

]