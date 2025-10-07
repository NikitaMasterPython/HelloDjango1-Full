from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_victory, name='victory'),
    path('bankrot/', views.check_victory_money, name='victory_money'),
    path('loyalty/', views.check_victory_loyalty, name='victory_loyalty'),
]