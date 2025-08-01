from django.urls import path
from . import views

urlpatterns = [
    path('', views.play_restart, name='play_restart'),

]