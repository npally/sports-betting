from django.contrib import admin
from .models import Game, Pick, Nba_Record
# Register your models here.

class GameAdmin(admin.ModelAdmin):
    model = Game
    list_per_page = 50



admin.site.register(Game, GameAdmin)
admin.site.register(Pick)
admin.site.register(Nba_Record)