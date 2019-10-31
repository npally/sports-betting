from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from datetime import date

import scripts
from .models import Game, Week, Pick, Nfl_Record
# Create your views here.

WEEK = 9

class NflMatchupView(LoginRequiredMixin, TemplateView):
    template_name = 'nfl_matchups.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u = self.request.user
        context['picks'] = Pick.objects.filter(user=u, game__week=WEEK)
        context['games'] = Game.objects.filter(week=WEEK)
        context['week'] = Week.objects.get(pk=WEEK)
        context['now'] = timezone.now()

        return context

def nfl_matchup_detail(request, pk):
    matchup = get_object_or_404(Game, pk=pk)

    if request.method == 'POST':
        g = 'game'+ str(matchup.id)
        spread = request.POST.get(g)
        user = request.user
        game = matchup

        picks = Pick.objects.filter(user=user, game__week=WEEK)
        wp = Pick.objects.filter(user=user, game__week=WEEK).count()
        for p in picks:
            if p.game == game:
                messages.error(request, 'This game has already been picked')
                return HttpResponseRedirect(reverse('nfl_matchups'))

        if wp > 2:
            messages.error(request, 'You can only choose 3 games per week')
            return HttpResponseRedirect(reverse('nfl_matchups'))

        pick = Pick(user=user, game=game, pick=spread)
        pick.save()

        return HttpResponseRedirect(reverse('nfl_matchups'))
    else:
        return render(request, 'nfl_matchup_detail.html', {'matchup': matchup})

class NflStandingsView(ListView):
    model = Nfl_Record
    template_name = 'nfl_standings.html'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recs = Nfl_Record.objects.filter(wins__gt=0)
        recs = sorted(recs, key=lambda x: x.get_winning_percentage(), reverse=True)
        context['recs'] = recs
        return context