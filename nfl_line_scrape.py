from bs4 import BeautifulSoup
import requests
import csv
import scripts
import sys
import os
import django

sys.path.append('spread')
os.environ['DJANGO_SETTINGS_MODULE'] = 'spread.settings'
django.setup()

from nfl.models import Game, Week

WEEK = scripts.get_week()
# deployment '/home/kilgoretrout1/spread/csv_files/spreads.csv'
SPREADS = 'csv_files/spreads.csv'
GAMES = 'csv_files/nfl_schedule.csv'

d = {'New Orleans': 'Saints', 'Pittsburgh': 'Steelers', 'New England': 'Patriots',
     'Tampa Bay': 'Buccaneers', 'Philadelphia': 'Eagles', 'Atlanta': 'Falcons', 'Cleveland': 'Browns',
     'Cincinnati': 'Bengals', 'Oakland': 'Raiders', 'Buffalo': 'Bills', 'NY Giants': 'Giants',
     'Detroit': 'Lions', 'LA Rams': 'Rams', 'Carolina': 'Panthers', 'San Francisco': '49ers',
     'Indianapolis': 'Colts', 'Seattle': 'Seahawks', 'Arizona': 'Cardinals', 'Houston': 'Texans',
     'Tennessee': 'Titans', 'Jacksonville': 'Jaguars', 'Chicago': 'Bears', 'LA Chargers': 'Chargers',
     'Miami': 'Dolphins', 'NY Jets': 'Jets', 'Baltimore': 'Ravens', 'Kansas City': 'Chiefs',
     'Denver': 'Broncos', 'Washington': 'Redskins', 'Green Bay': 'Packers', 'Minnesota': 'Vikings',
     'Dallas': 'Cowboys'}

matchups = []

source = "https://www.oddsshark.com/nfl/consensus-picks"
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

        for key, value in d.items():
            if team == key:
                team = value

        spread = line.find("td", class_="consensus-spread").text

        t = (team, spread)
        l.append(t)
    matchups.append(l)


for m in matchups:

    games = Game.objects.filter(week=WEEK)
    for game in games:
        at = m[0][0].split()[-1]
        ht = m[1][0].split()[-1]
        if at == game.away_team.split()[-1] and ht == game.home_team.split()[-1]:
            if m[0][1] == 'Ev':
                game.away_spread = float(0)
            else:
                game.away_spread = float(m[0][1])
            
            if m[1][1] == 'Ev':
                game.home_spread = float(0)
            else:
                game.home_spread = float(m[1][1])
            game.save()