
from django.urls import path
from . import views
# from play import views
# from play import views

urlpatterns = [
    path('play/', views.play, name='play'),
    path('event/<int:event_id>/', views.play_next, name='play_next'),
    path('event_end/<int:event_id>/', views.event_part_2, name='event_part_2'),
    path('random_event/', views.random_event, name='random_event'),
    path('consequence/<int:event_id>/<int:action>/', views.get_consequence, name='get_consequence'),
    path('use_herbs/', views.use_herbs, name='use_herbs'),




]