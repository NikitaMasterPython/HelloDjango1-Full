from django.urls import path
from . import views
from django.urls import path, include

app_name = 'quest'

urlpatterns = [
    path('', views.game_view, name='game'),
    path('tupic/', views.tupic_view, name='tupic'),
    path('scene/<int:scene_id>/', views.scene, name='scene'),
    path('make_choice/', views.make_choice, name='make_choice'),
    path('play_restart/', include('play_restart.urls')),

]