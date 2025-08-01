
from django.urls import path
from . import views

urlpatterns = [
    path('', views.check_death, name='death_page'),  # Простое имя маршрута без namespace
]
