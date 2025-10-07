
from django.urls import path
from . import views
# from play import views
# from market import views

urlpatterns = [
    path('play/', views.play, name='play'),


    path('event/<int:event_id>/', views.play_next, name='play_next'),
    path('event_end/<int:event_id>/', views.event_part_2, name='event_part_2'),
    path('random_event/', views.random_event, name='random_event'),
    path('consequence/<int:event_id>/<int:action>/', views.get_consequence, name='get_consequence'),


    path('use_herbs/', views.use_herbs, name='use_herbs'),
    path('use_Samogon/', views.use_Samogon, name='use_Samogon'),
    path('use_Poison/', views.use_Poison, name='use_Poison'),
    path('use_Fish/', views.use_Fish, name='use_Fish'),
    path('use_Jewelry/', views.use_Jewelry, name='use_Jewelry'),
    path('use_Harvest/', views.use_Harvest, name='use_Harvest'),





]