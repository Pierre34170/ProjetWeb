from django.contrib import admin
from team.models import Team, BelongToTeam

admin.site.register(Team)
admin.site.register(BelongToTeam)