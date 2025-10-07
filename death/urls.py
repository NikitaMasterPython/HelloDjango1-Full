from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_death, name='death'),
    path('bankrot/', views.check_bankrot, name='bankrot'),
    path('loyalty/', views.check_loyalty, name='loyalty_death'),
]
