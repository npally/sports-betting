from django.contrib import admin
from .models import Game
# Register your models here.

class GameAdmin(admin.ModelAdmin):
    model = Game
    list_per_page = 50


admin.site.register(Game, GameAdmin)
