from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from datetime import datetime
import csv
# Create your models here.
class Game(models.Model):
    home_team = models.CharField(max_length=30)
    away_team = models.CharField(max_length=30)
    home_spread = models.FloatField(null=True)
    away_spread = models.FloatField(null=True)
    date_time = models.DateTimeField()
    neutral = models.BooleanField()
    home_score = models.FloatField(null=True)
    away_score = models.FloatField(null=True)

    def __str__(self):
        dt = str(self.date_time)[:16]
        s = f"{dt} {self.away_team} vs. {self.home_team}"
        return s

    @classmethod
    def create(cls, home_team, away_team, date_time, neutral):
        game = cls(home_team=home_team, away_team=away_team, date_time=date_time, neutral=neutral)
        return game

    @classmethod
    def upload_games(cls):
        with open('csv_files/nba_games19-20.csv') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                home_team = row['home_team']
                away_team = row['away_team']

                date = row['date']
                time = row['time']
                dt = date + " " + time
                dt_object = datetime.strptime(dt, "%b %d, %Y %I:%M%p")
                aware_dt = timezone.make_aware(dt_object)

                neutral = False

                game = cls.create(home_team, away_team, aware_dt, neutral)
                game.save()

class Pick(models.Model):
    # user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    # game = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # pick = models.CharField(max_length=40)
    pass
