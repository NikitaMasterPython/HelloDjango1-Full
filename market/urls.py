from django.urls import path
from . import views

urlpatterns = [
    path('mybag/', views.mybag, name='mybag'),
    path('map/', views.map_0, name='map_0'),
    # path('get_player_status/', views.get_player_status, name='get_player_status'),


]