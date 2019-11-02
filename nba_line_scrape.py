from bs4 import BeautifulSoup
import requests
from datetime import date


import sys
import os
import django

sys.path.append('spread')
os.environ['DJANGO_SETTINGS_MODULE'] = 'spread.settings'
django.setup()

from nba.models import Game
from django.utils import timezone
today = timezone.now()
today = today.date()

teams = {'Atlanta': 'Atlanta Hawks', 'Boston': 'Boston Celtics', 'Brooklyn': 'Brooklyn Nets', 
         'Charlotte': 'Charlotte Hornets', 'Chicago': 'Chicago Bulls', 'Cleveland': 'Cleveland Cavaliers', 
         'Dallas': 'Dallas Mavericks', 'Denver': 'Denver Nuggets', 'Detroit': 'Detroit Pistons', 
         'Golden State': 'Golden State Warriors', 'Houston': 'Houston Rockets', 'Indiana': 'Indiana Pacers', 'LA Clippers': 'Los Angeles Clippers',
         'LA Lakers': 'Los Angeles Lakers', 'Memphis': 'Memphis Grizzlies', 'Miami': 'Miami Heat', 'Milwaukee': 'Milwaukee Bucks', 
         'Minnesota': 'Minnesota Timberwolves', 'New Orleans':'New Orleans Pelicans', 'New York': 'New York Knicks', 
         'Oklahoma City': 'Oklahoma City Thunder', 'Orlando': 'Orlando Magic', 'Philadelphia': 'Philadelphia 76ers', 'Phoenix': 'Phoenix Suns', 
         'Portland': 'Portland Trail Blazers', 'Sacramento': 'Sacramento Kings', 'San Antonio': 'San Antonio Spurs', 
         'Toronto': 'Toronto Raptors', 'Utah': 'Utah Jazz', 'Washington': 'Washington Wizards'}


matchups = []

source = "https://www.oddsshark.com/nba/consensus-picks"
page = requests.get(source)

soup = BeautifulSoup(page.text, 'lxml')

games = soup.find_all('tbody')
game = games[0]


for game in games:
    l = []
    for line in game:

        team = line.find("div", class_="name-wrap").text
        team = team.split()
        team = " ".join(team[1:])
        team = teams[team]

        

        spread = line.find("td", class_="consensus-spread").text

        t = (team, spread)
        l.append(t)
    matchups.append(l)


for m in matchups:

    games = Game.objects.filter(date_time__date=today)
    for game in games:
        if m[0][0] == game.away_team and m[1][0] == game.home_team:
            game.away_spread = float(m[0][1])
            game.home_spread = float(m[1][1])
            game.save()

        

