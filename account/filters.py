import django_filters


from .models import *

class TeamFilter(django_filters.FilterSet):
	class Meta: 
		model = Team 
		fields = '__all__'
		exclude = ['creator', 'nb_players', 'date_creation']