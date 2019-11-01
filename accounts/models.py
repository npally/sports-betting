from django.db import models
from django.contrib.auth import get_user_model
from nba.models import Pick as nba_pick
from nfl.models import Pick as nfl_pick


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    balance = models.FloatField(default=1000.00)
    init_balance = models.FloatField(default=1000.00)
    in_play = models.FloatField(default=0, null=True)

    def __str__(self):
        b = "{:.2f}".format(self.balance)
        s = f"{self.user.username}: ${b}"
        return s

    def calculate_balance(self):
        winnings = 0.0
        ip = 0.0
        picks = nba_pick.objects.filter(user=self.user)
        for pick in picks:
            
            if pick.wager is not None:
                if pick.outcome == 'win':
                    winnings += pick.wager
                    winnings += 10/11 * pick.wager
                elif pick.outcome == 'push':
                    winnings += pick.wager
                
                elif pick.outcome is None:
                    ip += pick.wager
        
        nfl_picks = nfl_pick.objects.filter(user=self.user)
        for pick in nfl_picks:
            
            if pick.wager is not None:
                if pick.outcome == 'win':
                    winnings += pick.wager
                    winnings += 10/11 * pick.wager
                elif pick.outcome == 'push':
                    winnings += pick.wager
                
                elif pick.outcome is None:
                    ip += pick.wager
            
                     
        self.in_play = ip        
        self.balance = winnings + self.init_balance


    def get_balance(self):
        b = "{:.2f}".format(self.balance)
        return b
    
    def get_in_play(self):
        ip = "{:.2f}".format(self.in_play)
        return ip

    def get_winnings(self):
        winnings = self.balance - self.init_balance + self.in_play
        return "{:.2f}".format(winnings)
    
    def check_balance(self, x):
        if self.balance - x >= 0:
            return True
        else:
            return False 

     
