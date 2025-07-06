from django.urls import path
from . import views

urlpatterns = [
    path('play_restart/', views.play_restart, name='play_restart'),
]