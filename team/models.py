from django.db import models
from django.urls import reverse
from account.models import Account


class Team (models.Model):
	name_team = models.CharField(verbose_name="Name", max_length=30, unique=True)
	number_players_max = models.PositiveIntegerField(verbose_name="number of players max", null=True)
	number_players = models.PositiveIntegerField(null=True)
	date_creation = models.DateTimeField(verbose_name='date creation', auto_now=True)
	creator = models.ForeignKey(Account, on_delete=models.CASCADE)

	def __str__(self):
		return self.name_team

	def get_absolute_url(self):
		return reverse('home')


class BelongToTeam (models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
	player = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

