from django.urls import path
from .views import NflMatchupView, NflStandingsView
from . import views

urlpatterns = [
    path('matchups/', NflMatchupView.as_view(), name='nfl_matchups'),
    path('matchups/<int:pk>', views.nfl_matchup_detail, name='nfl_matchup_detail'),
    path('standings/', NflStandingsView.as_view(), name='nfl_standings'),
]