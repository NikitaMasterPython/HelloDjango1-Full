from django.urls import path
from . import views

urlpatterns = [
    path('mybag/', views.mybag, name='mybag'),
]