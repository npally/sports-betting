from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta

import sys
import os
import django

sys.path.append('spread')
os.environ['DJANGO_SETTINGS_MODULE'] = 'spread.settings'
django.setup()

from nba.models import Game, Pick, Nba_Record

today = date.today()
yesterday = today - timedelta(days=1)

# deployment '/home/kilgoretrout1/spread/csv_files/results.csv'

teams = {'Atlanta': 'Atlanta Hawks', 'Boston': 'Boston Celtics', 'Brooklyn': 'Brooklyn Nets', 
         'Charlotte': 'Charlotte Hornets', 'Chicago': 'Chicago Bulls', 'Cleveland': 'Cleveland Cavaliers', 
         'Dallas': 'Dallas Mavericks', 'Denver': 'Denver Nuggets', 'Detroit': 'Detroit Pistons', 
         'Golden State': 'Golden State Warriors', 'Houston': 'Houston Rockets', 'Indiana': 'Indiana Pacers', 'LA Clippers': 'Los Angeles Clippers',
         'LA Lakers': 'Los Angeles Lakers', 'Memphis': 'Memphis Grizzlies', 'Miami': 'Miami Heat', 'Milwaukee': 'Milwaukee Bucks', 
         'Minnesota': 'Minnesota Timberwolves', 'New Orleans':'New Orleans Pelicans', 'New York': 'New York Knicks', 
         'Oklahoma City': 'Oklahoma City Thunder', 'Orlando': 'Orlando Magic', 'Philadelphia': 'Philadelphia 76ers', 'Phoenix': 'Phoenix Suns', 
         'Portland': 'Portland Trail Blazers', 'Sacramento': 'Sacramento Kings', 'San Antonio': 'San Antonio Spurs', 
         'Toronto': 'Toronto Raptors', 'Utah': 'Utah Jazz', 'Washington': 'Washington Wizards'}

source = f"https://www.basketball-reference.com/boxscores/?month={yesterday.month}&day={yesterday.day}&year={yesterday.year}"\

page = requests.get(source)

soup = BeautifulSoup(page.text, 'lxml')

tables = soup.find("div", class_="game_summaries")

games = tables.find_all("div", class_="game_summary expanded nohover")

scores = []
for game in games:
    score = []
    for td in game.find_all("td"):
        if td.text != "":
            score.append(td.text.strip())
    clean_score = score[:5] 
    clean_score[0] = teams[clean_score[0]]
    clean_score[3] = teams[clean_score[3]]
    clean_score.pop(2)       
    scores.append(clean_score)



for score in scores:
    games = Game.objects.filter(date_time__date=yesterday)
    for game in games:
        if score[0] == game.away_team and score[2] == game.home_team:
            game.away_score = float(score[1])
            game.home_score = float(score[3])
            game.save()


picks = Pick.objects.all()
for pick in picks:
    pick.get_outcome()
    pick.save()

records = Nba_Record.objects.all()

for rec in records:
    rec.update_record()
    rec.save()