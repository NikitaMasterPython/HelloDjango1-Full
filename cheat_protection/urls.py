from django.urls import path
from . import views

app_name = 'cheat_protection'

urlpatterns = [
    path('cheat_warning/', views.cheat_warning, name='cheat_warning'),
    path('return_to_game/', views.return_to_game, name='return_to_game'),
]