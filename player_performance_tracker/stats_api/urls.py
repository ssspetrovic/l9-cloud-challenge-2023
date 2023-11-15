from django.urls import path
from .views import PlayerStatsViewSet

urlpatterns = [
    path('stats/player/<str:player_name>/', PlayerStatsViewSet.as_view({'get': 'retrieve'})),
]