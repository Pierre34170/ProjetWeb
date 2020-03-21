import django_filters


from .models import *

class TeamFilter(django_filters.FilterSet):
	class Meta: 
		model = Team 
		fields = '__all__'
		exclude = ['creator', 'number_players', 'date_creation', 'number_players_max']