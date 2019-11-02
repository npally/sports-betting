from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import date

from .models import Game, Pick, Nba_Record
from accounts.models import Account

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'
    login_url = 'login'

class MatchupPageView(LoginRequiredMixin, TemplateView):
    template_name = 'matchups.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u = self.request.user
        context['picks'] = Pick.objects.filter(user=u, game__date_time__date=date.today())
        context['games'] = Game.objects.filter(date_time__date=date.today())
        context['today'] = date.today()
        context['now'] = timezone.now()

        return context



def matchup_detail(request, pk):
    matchup = get_object_or_404(Game, pk=pk)
   
    if request.method == 'POST':
        
        g = 'game'+ str(matchup.id)
        spread = request.POST.get(g)
        if spread is not None:
            wager = request.POST.get("wager")
            wager = float(wager)
            user = request.user
            game = matchup
            
            picks = Pick.objects.filter(user=user, game__date_time__date=date.today())
            for p in picks:
                if p.game == game:
                    messages.error(request, 'This game has already been picked')
                    return HttpResponseRedirect(reverse('nba_matchups'))


            account = Account.objects.get(user=user)
            
            if account.check_balance(wager):
                account.balance = account.balance - wager
                account.in_play += wager
                account.save()

                pick = Pick(user=user, game=game, pick=spread, wager=wager)
                pick.save()
                
                return HttpResponseRedirect(reverse('nba_matchups'))
            else:
                messages.error(request, "You don't have enough funds to place that bet.")
                return HttpResponseRedirect(reverse('nba_matchups'))

        else:
            messages.error(request, "You didn't choose a spread! Please try again.")
            return HttpResponseRedirect(reverse('nba_matchups'))
    else:
        return render(request, 'matchup_detail.html', {'matchup': matchup})


class NbaStandingsView(ListView):
    model = Nba_Record
    template_name = 'nba_standings.html'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recs = Nba_Record.objects.filter(wins__gt=0)
        recs = sorted(recs, key=lambda x: x.get_winning_percentage(), reverse=True)
        context['recs'] = recs
        return context
