from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.market, name='market'),

    path('buy_herbs/', views.buy_herbs, name='buy_herbs'),
    path('buy_samogon/', views.buy_samogon, name='buy_samogon'),
    path('buy_poison/', views.buy_poison, name='buy_poison'),
    path('buy_fish/', views.buy_fish, name='buy_fish'),
    path('buy_jewerly/', views.buy_jewelry, name='buy_jewelry'),
    path('buy_harvest/', views.buy_harvest, name='buy_harvest'),
    path('save_action/', views.save_market_action, name='save_market_action'),

]

