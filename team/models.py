from django.db import models
from django.urls import reverse
from account.models import Account


class Team (models.Model):
	libelle_team = models.CharField(max_length=30, unique=True)
	nb_players_max = models.PositiveIntegerField(null=True)
	nb_players = models.PositiveIntegerField(null=True)
	date_creation = models.DateTimeField(verbose_name='date creation', auto_now=True)
	creator = models.ForeignKey(Account, on_delete=models.CASCADE)

	def __str__(self):
		return self.libelle_team

	def get_absolute_url(self):
		return reverse('home')


class BelongToTeam (models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
	player = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

