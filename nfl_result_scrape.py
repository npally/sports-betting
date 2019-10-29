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

from nfl.models import Game, Pick, Nfl_Record

WEEK = scripts.get_week()
w = WEEK
source = "https://www.pro-football-reference.com/years/2019/week_{}.htm".format(
    w)

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
    scores.append(score[:6])

for score in scores:
    games = Game.objects.filter(week=WEEK)
    for game in games:
        if score[1] == game.away_team and score[4] == game.home_team:
            game.away_score = float(score[2])
            game.home_score = float(score[5])
            game.save()


picks = Pick.objects.all()
for pick in picks:
    pick.get_outcome()
    pick.save()

records = Nfl_Record.objects.all()

for rec in records:
    rec.update_record()
    rec.save()