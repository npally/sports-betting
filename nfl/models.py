from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

import csv
from datetime import datetime

import scripts
# Create your models here.
CSV = 'csv_files/nfl_schedule.csv'
# deployment '/home/kilgoretrout1/nba-picks/csv_files/nfl_schedule.csv'


class Week(models.Model):
    week = models.IntegerField()

    def __str__(self):
        return "Week {}".format(self.week)


class Game(models.Model):
    week = models.ForeignKey('Week', on_delete=models.CASCADE)
    home_team = models.CharField(max_length=30)
    away_team = models.CharField(max_length=30)
    home_spread = models.FloatField(null=True)
    away_spread = models.FloatField(null=True)
    date_time = models.DateTimeField()
    home_score = models.FloatField(null=True)
    away_score = models.FloatField(null=True)

    def __str__(self):
        dt = str(self.date_time)[:11]
        s = f"{dt} {self.week} {self.away_team} vs. {self.home_team}"
        return s

    class Meta:
        ordering = ['pk']
        
    @classmethod
    def create(cls,week, home_team, away_team, date_time):
        game = cls(week=week, home_team=home_team, away_team=away_team, date_time=date_time)
        return game

    @classmethod
    def upload_games(cls):
        with open(CSV) as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:

                w = row['week']
                week = Week.objects.get(pk=w)
                home_team = row['home_team']
                away_team = row['away_team']

                date = row['date']
                time = row['time']
                dt = date + " " + time
                dt_object = datetime.strptime(dt, "%m/%d/%y %I:%M%p")
                aware_dt = timezone.make_aware(dt_object)

                game = cls.create(week, home_team, away_team, aware_dt )
                game.save()

class Pick(models.Model):

    choices = [('win', 'win'),
               ('loss', 'loss'),
               ('push', 'push')
               ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='nfl_pick_user')
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    pick = models.CharField(max_length=40)
    outcome = models.CharField(max_length=5, choices=choices, null=True)
    
    def __str__(self):
        return "{} | {} {}".format(self.game, self.user, self.pick)

    def get_pick(self):
        points = float(self.pick.split()[-1])
        team = ' '.join(self.pick.split()[:-1])
        if points < 0:
            return "{} {}".format(team, points)
        elif points > 0:
            return "{} +{}".format(team, points)
    
    def get_outcome(self):
        info = self.pick.split()
        team = " ".join(info[:-1])
        line = info[-1]

        game = self.game

        if team == game.home_team:
            score = game.home_score + float(line)
            if score - game.away_score > 0:
                self.outcome = 'win'
            elif score - game.away_score < 0:
                self.outcome = 'loss'
            elif score - game.away_score == 0:
                self.outcome = 'push'
        
        elif team == game.away_team:
            score = game.away_score + float(line)
            if score - game.home_score > 0:
                self.outcome = 'win'
            elif score - game.home_score < 0:
                self.outcome = 'loss'
            elif score - game.home_score == 0:
                self.outcome = 'push'

class Nfl_Record(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    pushes = models.PositiveIntegerField(default=0)
    in_wins = models.PositiveIntegerField(default=0)
    in_losses = models.PositiveIntegerField(default=0)
    in_pushes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} NFL Record: {self.wins}-{self.losses}-{self.pushes}"

    def update_record(self):
        picks = Pick.objects.filter(user=self.user)
        w = 0
        l = 0
        p = 0
        for pick in picks:
            
            if pick.outcome == 'win':
                w += 1
            elif pick.outcome == 'loss':
                l += 1
            elif pick.outcome == 'push':
                p += 1
        self.wins = w + self.in_wins
        self.losses = l +self.in_losses
        self.pushes = p + self.in_pushes

    def get_winning_percentage(self):
        if self.wins + self.losses + self.pushes > 0:
            wp = round(float(self.wins/(self.wins + self.losses) * 100), 1)
            return wp
        else:
            return 0