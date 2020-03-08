from django.db import models
from account.models import Account
from team.models import Team
from django.utils import timezone
from django.urls import reverse


class Proposition(models.Model):
	title = models.CharField(max_length=300)
	date_posted = models.DateTimeField(default=timezone.now)
	date_match = models.DateField()
	hour_beggin = models.TimeField()
	lieu_match = models.CharField(max_length=300)
	name_stadium = models.CharField(max_length=50)
	author = models.ForeignKey(Account, null = True, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('proposition_detail', kwargs={'pk': self.pk})



class Reserve(models.Model):
	player = models.ForeignKey(Account, on_delete=models.CASCADE)
	proposition = models.ForeignKey(Proposition, on_delete=models.CASCADE)
	date_reservation = models.DateTimeField(default=timezone.now)



class Play(models.Model):
	game = models.ForeignKey(Proposition, null = True, on_delete=models.CASCADE)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	score = models.CharField(max_length=10, null = True)
