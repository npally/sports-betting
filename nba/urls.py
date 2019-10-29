from django.urls import path

from .views import HomePageView, MatchupPageView, NbaStandingsView
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('nba/matchups/', MatchupPageView.as_view(), name='nba_matchups'),
    path('nba/matchups/<int:pk>', views.matchup_detail, name='matchup_detail'),
    path('nba/standings/', NbaStandingsView.as_view(), name='nba_standings'),
]
