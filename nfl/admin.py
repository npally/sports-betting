from django.contrib import admin

from .models import Week, Game, Pick, Nfl_Record

# Register your models here.

admin.site.register(Game)
admin.site.register(Pick)
admin.site.register(Nfl_Record)