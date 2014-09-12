from django.contrib import admin
from ladder.models import PlayerProfile, DoublesTeamProfile, Match, MatchStats

# Register your models here.
admin.site.register(PlayerProfile)
admin.site.register(DoublesTeamProfile)
admin.site.register(Match)
admin.site.register(MatchStats)

