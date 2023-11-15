from django.urls import path
from .views import PlayerStatsView

urlpatterns = [
    path("stats/player/<str:player_name>/", PlayerStatsView.as_view()),
]
